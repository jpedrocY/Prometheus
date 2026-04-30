# Phase 3v — GAP-20260424-032 Stop-Trigger Domain Ambiguity Resolution Memo (docs-only)

**Authority:** GAP-20260424-032 (Phase 2f strategy review; `docs/00-meta/implementation-ambiguity-log.md`); Phase 2i §1.7.3 project-level locks (mark-price stops mandatory for live operation); Phase 2y §11.3.5 (no post-hoc loosening); Phase 2p §C.1 (R3 baseline-of-record); Phase 2w §16.1 (R2 FAILED — §11.6); Phase 3d-B2 (F1 HARD REJECT); Phase 3j §11.2 (D1-A MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3s §Q6 (D1-A mark-stop lag empirical evidence); Phase 3t (5m research thread closure); Phase 3u §8 (pre-coding blocker review highlighting GAP-20260424-032 as HIGH-priority); `docs/07-risk/stop-loss-policy.md`; `docs/06-execution-exchange/binance-usdm-order-model.md`; `docs/06-execution-exchange/exchange-adapter-design.md`; `docs/03-strategy-research/v1-breakout-strategy-spec.md` (line 332); `docs/03-strategy-research/v1-breakout-backtest-plan.md` (§Stop trigger reference, lines 180–181); `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 3v — Docs-only **GAP-20260424-032 stop-trigger domain ambiguity resolution memo.** Resolves the governance ambiguity between historical backtest stop-trigger provenance (trade-price-modeled, per `docs/03-strategy-research/v1-breakout-backtest-plan.md` §Stop trigger reference) and future runtime / paper / live stop-trigger policy (mark-price-locked per §1.7.3 + `docs/07-risk/stop-loss-policy.md` + `docs/06-execution-exchange/binance-usdm-order-model.md`). **Phase 3v writes no implementation code; modifies no runtime / strategy / execution / risk-engine / database / dashboard / exchange code; runs no diagnostics; runs no backtests; acquires no data; modifies no manifests; modifies no v002 datasets / manifests; modifies no Phase 3q v001-of-5m manifests; revises no retained-evidence verdict; modifies no §11.6 / §1.7.3 lock; proposes no strategy rescue; proposes no new strategy candidate; authorizes no Phase 4 / 4a / paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write capability.**

**Branch:** `phase-3v/gap-20260424-032-stop-trigger-domain-resolution`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim.

---

## 1. Summary

GAP-20260424-032 records that Prometheus historical backtests use trade-price bars to model stop-trigger events while the live execution model uses Binance `workingType=MARK_PRICE` stop-trigger semantics. This is a real *domain mismatch* between historical evidence provenance and live-runtime stop-trigger policy. Phase 2f scoped it as Pre-paper-shadow (HIGH-risk per Phase 3u §8.5). Phase 3s §Q6 produced empirical evidence about the magnitude of the gap on the v002-locked retained-evidence trade populations (D1-A mark-stops lag trade-stops by ~1.3–1.8 5m-bars; R3 / R2 / F1 are within 1 5m-bar mean-lag). Phase 3u §8 flagged GAP-20260424-032 as the highest-priority pre-coding blocker.

Phase 3v formally resolves the governance question by writing a concrete rule into the project record. The rule has eight clauses (§7 below). In summary:

1. **Historical retained-evidence backtests remain valid only under their original trade-price-stop-provenance.** The verdict provenance is unchanged. R3 / R2 / F1 / D1-A verdicts are NOT revised.
2. **Future runtime / paper / live stop handling remains mark-price-locked.** Per §1.7.3 + `docs/07-risk/stop-loss-policy.md`. Phase 3v does NOT modify the lock.
3. **Stop-trigger domain becomes an explicit label** that future evidence and runtime artifacts must carry. `stop_trigger_domain ∈ {trade_price_backtest, mark_price_runtime, mark_price_backtest_candidate}`. **`mixed_or_unknown` fails closed** at any decision boundary.
4. **Future backtests intended to support paper/shadow/live readiness must explicitly use or validate mark-price stop-trigger modeling, or disclose that they are not live-readiness evidence.**
5. **Phase 3s Q6 remains descriptive only.** It does not revise verdicts, change stop-policy, or authorize strategy rescue.
6. **Future Phase 4a (if ever authorized) may implement the labels and fail-closed validation locally**, but Phase 4a must not place orders, must not implement exchange-write, and must not imply paper-shadow / live-readiness.
7. **GAP-20260424-032 is RESOLVED in the ambiguity log** by reference to this memo; the resolution preserves all locks, all verdicts, and all prior phase recommendations.

Phase 3v does not authorize Phase 4 / 4a / paper-shadow / live-readiness / deployment / production-key / exchange-write. The resolution is procedural: it makes the project's response to the trade-price-vs-mark-price domain mismatch fully explicit and binding on any future evidence or runtime artifact, without acting on it.

**Recommended state remains paused.**

---

## 2. Authority and boundary

Phase 3v operates strictly inside the post-Phase-3u boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5 / §6 / §7 / §10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation conclusions; Phase 3u §10 / §11 prohibitions on Phase 4 / 4a unauthorized scope. Nothing is revised.
- **Phase-gate governance respected.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 follows Phase 3 strategy evidence; Phase 3v does not authorize Phase 4 / 4a.
- **Project-level locks preserved verbatim.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md` — including stop widening forbidden, exchange-write before approved gate forbidden, production keys during early phases forbidden, blind retry forbidden, etc.
- **Stop-loss policy preserved verbatim.** `docs/07-risk/stop-loss-policy.md` + `docs/06-execution-exchange/binance-usdm-order-model.md` mark-price stop discipline preserved.

Phase 3v adds *governance language* (a formal stop-trigger-domain reconciliation rule) that resolves an existing OPEN ambiguity-log item without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate.

---

## 3. Starting state

```text
branch:           phase-3v/gap-20260424-032-stop-trigger-domain-resolution
parent commit:    4577d7506dc7de8d2d4108c4c63519ddc99ec0d9 (post-Phase-3u-merge housekeeping)
working tree:     clean
main:             4577d7506dc7de8d2d4108c4c63519ddc99ec0d9 (unchanged)

ambiguity log:    GAP-20260424-032 currently OPEN (Phase 3u §8.5 highest-priority pre-coding blocker).
phase-gate state: Phase 4 unauthorized; Phase 4a conditional only and not authorized.
research thread:  5m research thread operationally complete (Phase 3t).
v002 datasets:    locked; manifests untouched.
v001-of-5m:       trade-price research-eligible; mark-price research_eligible:false.
locks:            §11.6 = 8 bps HIGH per side; §1.7.3 mark-price stops; all preserved.
```

No code under `src/prometheus/` modified by Phase 3v. No script modified. No `data/` artefact modified. No prior-phase report modified. No strategy spec / threshold / project-lock / prior verdict modified.

---

## 4. Ambiguity being resolved

**GAP-20260424-032 — Backtest uses trade-price stops; live uses MARK_PRICE stops.**

Original entry (per `docs/00-meta/implementation-ambiguity-log.md`):

> **Description.** The live protective stop uses `workingType=MARK_PRICE` (spec line 332, per the Binance USDⓈ-M order model). The backtest plan specifies that the primary backtest simulation uses trade-price bars, with mark-price sensitivity as a separate, explicitly scoped sensitivity test (backtest-plan §Stop trigger reference, lines 180–181). The Phase 2e baseline reports zero stop gap-through events under the trade-price model; whether the same is true under a mark-price stop-trigger model is not yet measured.
>
> **Why it matters.** Any promotion claim that depends on stop behavior is fragile if only trade-price stop simulation has been done. For Phase 2f (docs-only, no runs), the GAP is non-blocking. For any future variant wave that intends to promote a candidate toward paper/shadow, a mark-price stop-trigger sensitivity must be part of the required report cuts, not an optional extra.

Phase 3u §8.5 reclassified GAP-20260424-032 as the **highest-priority pre-coding blocker**, citing:

- HIGH risk classification.
- Backtest verdicts produced under one stop-trigger model (trade-price); live operation will use a different model (mark-price, per §1.7.3).
- Phase 3s Q6 finding (D1-A mark-stop lag ~1.3–1.8 5m bars) directly characterizes the *magnitude* of the gap on retained-evidence trade populations.
- Pre-coding blocker for any future runtime; pre-paper-shadow blocker for any live work.

Phase 3v's task is to write a formal resolution that:
- Preserves the validity of historical evidence under its original trade-price provenance.
- Preserves the mark-price-stop policy lock for any future runtime / paper / live operation.
- Forces stop-trigger domain to be *explicit* in any future evidence or runtime artifact.
- Closes GAP-20260424-032 in the ambiguity log as RESOLVED via Phase 3v reference.
- Does not authorize any successor phase, any verdict revision, or any policy change.

---

## 5. Historical backtest stop-trigger provenance

### 5.1 What the historical backtests actually did

Per `docs/03-strategy-research/v1-breakout-backtest-plan.md` §Stop trigger reference (lines 180–181):

- The primary backtest simulation uses **trade-price bars** to model stop-trigger events. A trade-price 15m kline is the source-of-truth for whether a stop level was breached during a 15m interval.
- Mark-price stop-trigger sensitivity was specified as a **separately scoped sensitivity test**, not as the primary stop-trigger model.

This convention applies across all retained-evidence Phase 2 / Phase 3 backtests that produced the V1 / F1 / D1-A verdicts:

- **R3** (Phase 2l-r3-r baseline-of-record): trade-price stop-trigger provenance.
- **R1a, R1b-narrow** (Phase 2m / 2s): trade-price stop-trigger provenance.
- **R2** (Phase 2w): trade-price stop-trigger provenance. The §11.6 cost-sensitivity gate FAILED at HIGH slippage *under trade-price stop-trigger modeling*.
- **F1** (Phase 3d-B2): trade-price stop-trigger provenance. The catastrophic-floor predicate (Phase 3c §7.3) was evaluated under trade-price stop-trigger modeling.
- **D1-A** (Phase 3j): trade-price stop-trigger provenance. The cond_i / cond_iv FRAMEWORK FAIL — other was evaluated under trade-price stop-trigger modeling.

### 5.2 What this provenance means

- Historical verdicts are valid evidence about *what would have happened with trade-price-triggered stops* on the v002 historical date range.
- Historical verdicts are NOT direct evidence about *what would happen with mark-price-triggered stops* on the same date range or any future date range.
- The two domains can diverge — Phase 3s Q6 quantified the magnitude (D1-A: ~1.3–1.8 5m bars; R3 / R2 / F1: < 1 bar mean-lag).

### 5.3 Why historical verdicts remain valid despite the domain mismatch

Phase 3v does NOT propose revising historical verdicts because:

1. **The verdicts were produced under a documented, predeclared stop-trigger convention.** Phase 2y §11.3.5 (no post-hoc loosening) applies categorically: revising a verdict because of a domain re-classification *after the fact* is exactly the post-hoc loosening pattern Phase 2y forbids.
2. **The verdicts were terminal under their stop-trigger convention.** R2 FAILED — §11.6 was conclusive at HIGH slippage *under trade-price stops*; even if a mark-price-stop sensitivity were available, it would constitute *additional evidence*, not a *revision* of the trade-price-stop verdict.
3. **The R3 baseline-of-record is similarly trade-price-stop-provenance.** Promoting a different candidate by revising R3's domain would compromise framework discipline.
4. **Phase 3s Q6 informative finding for D1-A is descriptive only.** It does not by itself revise D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict (Phase 3p §8.6 / Phase 3r §8 / Phase 3s §6 / Phase 3t §8.6 all preserve this).

The historical verdicts therefore stand as *trade-price-stop-provenance evidence* with their original framework-gate semantics intact.

---

## 6. Runtime / paper / live stop-trigger policy

### 6.1 What §1.7.3 + stop-loss-policy locks require

- **§1.7.3 project-level lock:** mark-price stops (a `.claude/rules/prometheus-safety.md`-recorded project lock).
- **`docs/07-risk/stop-loss-policy.md`:** protective stops use `STOP_MARKET` orders with `workingType=MARK_PRICE` and `priceProtect=TRUE` per `docs/06-execution-exchange/binance-usdm-order-model.md`.
- **`.claude/rules/prometheus-safety.md`:** stop widening is forbidden in v1 categorically; mark-price stops are the canonical live stop-trigger discipline.

These three sources together establish that **any future runtime / paper / live phase must use mark-price-triggered stops, period.** No exception. No substitution. No silent trade-price-triggered fallback.

### 6.2 What this requires of any future runtime

- Stop placement must use Binance `STOP_MARKET` with `workingType=MARK_PRICE` and `priceProtect=TRUE`.
- Stop-trigger evaluation must use mark-price reference (not trade-price tape).
- Any backtest used as live-readiness evidence must either model mark-price stop-triggers explicitly, or disclose that it does not constitute live-readiness evidence.
- Any sensitivity analysis must label its stop-trigger domain explicitly.

### 6.3 Why the lock is preserved

The mark-price-stop lock exists to mitigate trade-tape manipulation risk. Mark-price is computed from a weighted average of multiple price sources and is intentionally smoothed; trade-tape is more easily manipulable on a per-trade basis. Live operation uses mark-price for liquidation reference (per Binance USDⓈ-M futures conventions); aligning stop-trigger domain with liquidation domain is a basic safety property. The Phase 3s Q6 finding (D1-A mark-stops trigger systematically *later* than trade-stops would; ~6–9 minutes lag) is consistent with mark-price's design philosophy — the lag is not a bug, it is the safety property.

§1.7.3 mark-price-stop lock is preserved verbatim by Phase 3v.

---

## 7. Phase 3s Q6 evidence relevance

Phase 3s Q6 produced empirical mark-vs-trade stop-trigger timing-difference statistics on the v002-locked retained-evidence STOP-exited trade populations, applying the Phase 3r §8 invalid-window exclusion rule (zero exclusions empirically). The verdicts (per Phase 3s §Q6 / Phase 3p §8.6):

| Candidate | Symbol | Mean (mark − trade) bars | Verdict |
|---|---|---|---|
| R3 | BTC | +0.125 | non-informative (< 1 bar) |
| R3 | ETH | +0.286 | non-informative |
| R2 | BTC | 0.000 | non-informative |
| R2 | ETH | +0.400 | non-informative |
| F1 | BTC | +0.373 | non-informative |
| F1 | ETH | +0.353 | non-informative |
| D1-A | BTC | **+1.252** | **informative** |
| D1-A | ETH | **+1.783** | **informative** |

**Q6 binding constraints (preserved by Phase 3v):**

- D1-A's informative Q6 finding is **descriptive only**. It does NOT revise D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict.
- D1-A's mark-stop lag does NOT authorize a D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or any other successor strategy.
- D1-A's mark-stop lag does NOT authorize stop-policy revision. §1.7.3 mark-price-stop lock is preserved.
- R3 / R2 / F1 non-informative Q6 findings mean the trade-price-vs-mark-price domain mismatch is *empirically small* for those candidates on v002 — but the procedural domain mismatch remains, regardless of magnitude.
- Q6 does NOT authorize strategy rescue, parameter change, threshold revision, or live-readiness implication (Phase 3p §8.6 / Phase 3r §8 / Phase 3s §6 / Phase 3t §8.6).

Phase 3v's role with respect to Q6:
- Q6 remains *one piece* of mechanism-level descriptive evidence in the project record.
- Q6 informs the *governance reconciliation* (§5.3 / §6.3 / §8 below) but does NOT drive verdict revision or policy change.
- Q6 is not the basis for the Phase 3v rule; the rule rests on §1.7.3 + stop-loss-policy + safety-rules-recorded discipline. Q6 is corroborating evidence about the magnitude of the issue, not the source of the rule.

---

## 8. Formal resolution

The following formal rule is the **stop-trigger domain governance rule** that Phase 3v writes into the project record. It is named **"GAP-20260424-032 resolution rule (Phase 3v §8)"** and is binding on any future evidence or runtime artifact from this commit forward.

### Rule statement

#### 8.1 Historical backtests retain trade-price-stop-provenance

Historical retained-evidence backtests (Phase 2e through Phase 3j, including R3 / R1a / R1b-narrow / R2 / F1 / D1-A) remain valid only under their original provenance:

- Stop-trigger domain: **`trade_price_backtest`** (canonical label).
- Dataset provenance: v002 historical datasets.
- Verdict provenance: unchanged.

Any future analysis that re-uses these populations must explicitly label them with the canonical stop-trigger domain or fail closed.

#### 8.2 Historical verdicts are not revised

The Phase 3v rule does not by itself revise any historical verdict:

- **R3** remains V1 breakout baseline-of-record per Phase 2p §C.1.
- **R2** remains FAILED — §11.6 cost-sensitivity blocks per Phase 2w §16.1.
- **F1** remains HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal.
- **D1-A** remains MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2; Phase 3j terminal under current locked spec.
- **H0** remains V1 breakout framework anchor.
- **R1a / R1b-narrow** remain retained research evidence only; non-leading.

No retained-evidence verdict is reopened by Phase 3v. Any future operator decision to authorize a formal reclassification phase (separate, predeclared evidence thresholds) is a separate authorization and is NOT contemplated by Phase 3v.

#### 8.3 Future runtime / paper / live stop handling remains MARK_PRICE-locked

Mark-price stops remain the canonical runtime / live stop-trigger domain per:

- §1.7.3 project-level locks.
- `docs/07-risk/stop-loss-policy.md`.
- `docs/06-execution-exchange/binance-usdm-order-model.md` (`workingType=MARK_PRICE`, `priceProtect=TRUE`).
- `.claude/rules/prometheus-safety.md` (mark-price stops; stop widening forbidden).

No future live / paper / runtime phase may silently use trade-price-triggered stops. Any future runtime must make stop-trigger domain explicit in code, configuration, persistence, and observability outputs.

#### 8.4 Stop-trigger domain becomes an explicit label

Future evidence and runtime artifacts must carry a `stop_trigger_domain` field. The valid values are:

- **`trade_price_backtest`** — the canonical label for historical Phase 2 / Phase 3 backtests (and any future research backtest that uses trade-price stop-trigger modeling for comparability with historical evidence).
- **`mark_price_runtime`** — the canonical label for any future runtime / paper / live stop-trigger pathway. Required for any artifact that claims live-readiness relevance.
- **`mark_price_backtest_candidate`** — the canonical label for any future research backtest that explicitly models mark-price stop-triggers (e.g., a separately authorized mark-price stop-trigger sensitivity analysis on existing v002 trade populations, or a new backtest using mark-price-triggered stops). Required label for any backtest evidence that intends to inform live-readiness claims.

The label **`mixed_or_unknown`** is **invalid** in any decision-relevant context. Any artifact that cannot determine its stop-trigger domain unambiguously must **fail closed** at the decision boundary. Specifically:

- A trade-execution decision under `mixed_or_unknown` must block the trade.
- A verdict decision under `mixed_or_unknown` must block the verdict.
- A persistence decision under `mixed_or_unknown` must block the persist.
- An evidence-promotion decision under `mixed_or_unknown` must block the promotion.

Fail-closed is the only acceptable response to ambiguous stop-trigger domain.

#### 8.5 Future backtests intended to support paper/shadow/live readiness

Any future backtest intended to support paper/shadow/live-readiness claims must:

- Either explicitly use mark-price stop-trigger modeling (`stop_trigger_domain = mark_price_backtest_candidate`), OR
- Explicitly disclose that it uses trade-price stop-trigger modeling and that it does NOT constitute live-readiness evidence (`stop_trigger_domain = trade_price_backtest`; live-readiness disclaimer in the report).

A backtest cannot simultaneously claim live-readiness relevance and use trade-price stop-triggers. The two are mutually exclusive.

#### 8.6 Phase 3s Q6 remains descriptive evidence only

Phase 3s Q6 findings:

- D1-A: mark-price stops trigger ~1.3–1.8 5m bars (~6–9 minutes) after trade-price stops would have triggered. Both BTC and ETH symbols informative.
- R3 / R2 / F1: non-informative; mark-vs-trade timing difference < 1 5m bar mean-lag.

These findings are descriptive evidence about the magnitude of the trade-vs-mark domain mismatch on retained-evidence trade populations. They are bound by the following preservations:

- **Q6 does NOT revise verdicts.** R3 / R2 / F1 / D1-A all preserved.
- **Q6 does NOT authorize stop-policy changes.** §1.7.3 mark-price-stop lock preserved. `docs/07-risk/stop-loss-policy.md` unchanged.
- **Q6 does NOT authorize strategy rescue.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, or any other successor authorized.
- **Q6 does NOT authorize live-readiness, paper-shadow, Phase 4, deployment, production-key creation, or exchange-write capability.**

#### 8.7 Future Phase 4a implication

If a future Phase 4a (safe-slice scoping per Phase 3u §11) is ever authorized — and Phase 3v does NOT authorize Phase 4a — Phase 4a may include local implementation of the §8.4 stop-trigger-domain labels and §8.4 fail-closed validation, subject to the Phase 3u §10 prohibitions:

- **Phase 4a must not place orders.**
- **Phase 4a must not implement exchange-write.**
- **Phase 4a must not imply paper/shadow or live-readiness.**
- **Phase 4a must not use production keys, authenticated APIs, private endpoints, user stream, WebSocket, or credentials.**
- **Phase 4a must not enable MCP / Graphify / `.mcp.json`.**
- **Phase 4a must not propose strategy rescue or new strategy candidates.**
- **Phase 4a must not relax §1.7.3, §10.3 / §10.4 / §11.3 / §11.4 / §11.6, mark-price-stop lock, or any other lock.**

Phase 4a is a strict subset of canonical Phase 4 with explicit anti-live-readiness preconditions; the §8 Phase 3v rule labels become enforceable in code at the Phase 4a layer if and only if Phase 4a is ever authorized.

#### 8.8 GAP-20260424-032 ambiguity-log resolution

GAP-20260424-032 should be resolved in `docs/00-meta/implementation-ambiguity-log.md` as:

- **Status:** RESOLVED (governance resolution per Phase 3v).
- **Resolution evidence:** Phase 3v memo (`docs/00-meta/implementation-reports/2026-04-30_phase-3v_gap-20260424-032-stop-trigger-domain-resolution.md`).
- **Resolution summary:** Historical backtests remain trade-price-stop-provenance evidence; future runtime / paper / live stop policy remains mark-price-locked per §1.7.3 + `docs/07-risk/stop-loss-policy.md`; future evidence and runtime artifacts must label stop-trigger domain explicitly (`trade_price_backtest` | `mark_price_runtime` | `mark_price_backtest_candidate`); `mixed_or_unknown` fails closed at any decision boundary; no retained-evidence verdict revised; Phase 3s Q6 remains descriptive only; future Phase 4a may implement labels and fail-closed validation locally subject to Phase 3u §10 prohibitions.

The ambiguity-log update is the only `docs/00-meta/implementation-ambiguity-log.md` modification authorized by Phase 3v.

---

## 9. Required stop-trigger domain labels

The §8.4 label scheme is repeated here in compact form for ease of reference:

| Label | Meaning | Required for |
|---|---|---|
| `trade_price_backtest` | Historical or research backtest using trade-price stop-trigger modeling. | All Phase 2 / Phase 3 retained-evidence backtests; any future research backtest comparable to historical evidence. |
| `mark_price_runtime` | Future runtime / paper / live stop-trigger pathway using `workingType=MARK_PRICE`. | Any artifact claiming live-readiness relevance; any future Phase 4a / Phase 6 / Phase 7 / Phase 8 / Phase 9 runtime. |
| `mark_price_backtest_candidate` | Research backtest explicitly modeling mark-price stop-triggers. | Any backtest evidence intended to support live-readiness claims. |
| `mixed_or_unknown` | Ambiguous or undeclared stop-trigger domain. **INVALID**. | None. **Fails closed at any decision boundary.** |

Future runtime, evidence, and operator-facing reports must include `stop_trigger_domain` as a first-class label. The label appears in:

- Backtest report manifests (`backtest_report.manifest.json` `config_snapshot`).
- Runtime persistence schemas (per `docs/08-architecture/runtime-persistence-spec.md` for any future runtime).
- Runtime event contracts (per `docs/08-architecture/internal-event-contracts.md` for any future runtime).
- Dashboard read models (per `docs/11-interface/operator-dashboard-requirements.md` for any future runtime).
- Trade-execution decisions (any future runtime).
- Risk-engine validations (any future runtime).
- Operator-facing alert messages (any future runtime).

The label requirement is binding from the Phase 3v commit forward. Existing artifacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs) **are not retroactively modified by Phase 3v**. The label requirement applies prospectively to any new artifact created from the Phase 3v commit forward.

For audit purposes, existing Phase 2 / Phase 3 retained-evidence backtest reports should be treated as having an *implicit* `stop_trigger_domain = trade_price_backtest` label (consistent with their actual provenance per Phase 3v §5.1). This implicit-label convention is documentary only; no manifest is rewritten.

---

## 10. Implications for retained verdicts

| Verdict | Original framework-gate provenance | Stop-trigger domain | Phase 3v action |
|---|---|---|---|
| **R3** baseline-of-record | Phase 2p §C.1 PROMOTE — broad-based | `trade_price_backtest` (implicit) | **Preserved verbatim.** Phase 3v writes no revision. |
| **H0** framework anchor | Phase 2i §1.7.3 | `trade_price_backtest` (implicit) | **Preserved verbatim.** |
| **R1a** retained research evidence | Phase 2m mixed-PROMOTE | `trade_price_backtest` (implicit) | **Preserved verbatim.** |
| **R1b-narrow** retained research evidence | Phase 2s formal-PROMOTE; non-leading | `trade_price_backtest` (implicit) | **Preserved verbatim.** |
| **R2** FAILED — §11.6 cost-sensitivity blocks | Phase 2w §16.1 | `trade_price_backtest` (implicit) | **Preserved verbatim.** |
| **F1** HARD REJECT | Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal | `trade_price_backtest` (implicit) | **Preserved verbatim.** |
| **D1-A** MECHANISM PASS / FRAMEWORK FAIL — other | Phase 3h §11.2; Phase 3j terminal under current locked spec | `trade_price_backtest` (implicit) | **Preserved verbatim.** |

**No retained-evidence verdict is reopened, revised, weakened, or strengthened by Phase 3v.** Phase 3v is a procedural / governance memo, not a verdict-revision phase. Any future operator decision to authorize a formal reclassification phase would be separately scoped, separately authorized, and subject to all predeclared discipline (Phase 2y §11.3.5 + Phase 3o §6 + Phase 3p §8 + Phase 3r §8 + Phase 3t §9 / §13 + Phase 3u §10).

---

## 11. Implications for future backtests

If the operator ever authorizes a future backtest phase, the Phase 3v rule requires:

### 11.1 Stop-trigger domain must be predeclared in the phase brief

Any future backtest phase brief must explicitly state which `stop_trigger_domain` value the phase will produce evidence for. Acceptable values are `trade_price_backtest` or `mark_price_backtest_candidate`. Mixed-domain phases are not authorized (a single phase may not produce both labels in the same artifact).

### 11.2 Live-readiness disclosure must accompany trade-price-stop backtests

Any future backtest with `stop_trigger_domain = trade_price_backtest` must include in its report a live-readiness disclosure:

> "This backtest uses trade-price stop-trigger modeling. It is research evidence for comparability with historical Phase 2 / Phase 3 retained-evidence backtests. It does NOT constitute live-readiness evidence per Phase 3v §8.5. Live-readiness evidence requires `mark_price_backtest_candidate` modeling per the §1.7.3 mark-price-stop lock + `docs/07-risk/stop-loss-policy.md`."

### 11.3 Mark-price-stop backtests must explicitly model mark-price triggers

Any future backtest with `stop_trigger_domain = mark_price_backtest_candidate` must explicitly:

- Source mark-price 5m / 15m / other-interval kline data (e.g., from Phase 3q v001-of-5m datasets if research-eligible, or from v002 mark-price 15m datasets).
- Implement stop-trigger evaluation against mark-price (not trade-price).
- Document the data version provenance for the mark-price source.
- If using Phase 3q v001-of-5m mark-price datasets: respect Phase 3r §8 invalid-window exclusion rule (those datasets are `research_eligible: false` per Phase 3r §8 governance; mark-price-backtest-candidate use is conditional on §8 exclusion).
- If using v002 mark-price 15m datasets: note that v002 mark-price 15m has the same 4 maintenance-window gaps as v001-of-5m (per Phase 3q §4.4 and Phase 3t §4.4); the same exclusion discipline applies.

### 11.4 Cross-domain comparability is bounded

A `mark_price_backtest_candidate` cannot be directly compared verdict-for-verdict against a `trade_price_backtest` candidate without explicit caveats. The Phase 3v rule does NOT permit silent re-labeling: any cross-domain comparison must explicitly call out that the two domains differ, and must apply Phase 2f Gate 1 / §11.3 / §11.6 framework discipline separately for each domain.

### 11.5 Phase 3v does not authorize any future backtest

The above are *prospective rules* for any backtest the operator may authorize later. Phase 3v itself does NOT authorize any future backtest, mark-price sensitivity analysis, or re-evaluation of retained-evidence populations.

---

## 12. Implications for future Phase 4a / runtime work

If a future Phase 4a (or any subsequent runtime phase) is ever authorized (and Phase 3v does NOT authorize Phase 4a), the Phase 3v rule requires:

### 12.1 Stop-trigger domain enforcement at runtime

Any runtime stop-trigger code path must:

- Use mark-price as the stop-trigger reference (`workingType=MARK_PRICE` per `docs/06-execution-exchange/binance-usdm-order-model.md`).
- Tag every stop event with `stop_trigger_domain = mark_price_runtime` in event contracts and persistence.
- Reject any stop event that cannot be unambiguously labeled (`mixed_or_unknown` → fail closed → block the trade).
- Validate that protective stop placement uses `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE` per the existing `docs/07-risk/stop-loss-policy.md` discipline.

### 12.2 Backtest-vs-runtime domain separation

Any runtime that consumes backtest verdicts as inputs (e.g., a strategy-readiness gate) must check that the source backtest's `stop_trigger_domain` matches the runtime requirement:

- For paper/shadow/live runtime: source backtest must be `mark_price_backtest_candidate` OR explicitly labeled as not-live-readiness.
- For research-only runtime / dry-run: either domain is acceptable as long as the runtime does not claim live-readiness.

### 12.3 Phase 4a implementation prohibition list (preserved from Phase 3u §10)

Phase 4a, if ever authorized, must NOT:

- Place orders.
- Implement exchange-write capability.
- Use production keys, authenticated APIs, private endpoints, user stream, or WebSocket.
- Enable MCP / Graphify / `.mcp.json`.
- Propose strategy rescue or new strategy candidates.
- Relax §1.7.3, §10.3 / §10.4 / §11.3 / §11.4 / §11.6, mark-price-stop lock, or any other lock.
- Imply paper/shadow / live-readiness / deployment / production-key / exchange-write authorization.

### 12.4 The §8.4 label scheme is enforceable in code

When and if Phase 4a is ever authorized, the §8.4 stop-trigger-domain labels become enforceable in code at the runtime persistence layer, the runtime event-contract layer, the risk-engine validation layer, and the dashboard / observability layer. The fail-closed semantics for `mixed_or_unknown` must be implemented as code-level constraints, not just policy text.

### 12.5 Phase 3v does not authorize Phase 4a

The above are *prospective rules* for any Phase 4a / runtime the operator may authorize later. Phase 3v itself does NOT authorize Phase 4a, runtime implementation, or any code change.

---

## 13. What this does not authorize

Phase 3v explicitly does NOT authorize, propose, or initiate any of the following:

- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **Threshold revision.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 all preserved verbatim.
- **Project-lock revision.** §1.7.3 mark-price-stop lock and all other §1.7.3 locks preserved verbatim.
- **Stop-loss-policy revision.** `docs/07-risk/stop-loss-policy.md` substantive content preserved verbatim. Phase 3v allows only an optional minimal cross-reference update (a back-pointer to this Phase 3v memo), not a substantive policy change.
- **Strategy-parameter revision.** R3 / R2 / F1 / D1-A specs preserved verbatim.
- **Strategy rescue.** No R2 / F1 / D1-A successor authorized. No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or 5m-on-X variant proposed.
- **5m strategy / hybrid / variant.** Phase 3o §4.1 / Phase 3p §10 prohibition preserved.
- **New strategy candidate.** Phase 3t §14.2 / Phase 3u §14 fresh-hypothesis-research-paused recommendation stands.
- **Phase 4 / Phase 4a authorization.** Phase 3u §16 recommendations stand; Phase 4 remains unauthorized; Phase 4a remains conditional only and not authorized.
- **Backtest re-running / mark-price sensitivity analysis.** Any future mark-price-stop sensitivity analysis on existing v002 trade populations would be a separately authorized phase.
- **Manifest re-issue.** All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` flag preserved.
- **Phase 3p §4.7 amendment.** Preserved verbatim.
- **Phase 3o / 3p / 3r / 3s / 3t / 3u rule modification.** All predeclared rules preserved.
- **Implementation.** No runtime, strategy, execution, risk, persistence, dashboard, observability, or test code changed.
- **Backtests.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No control rerun. No retained-evidence trade population regenerated.
- **ML feasibility.** Not authorized.
- **Regime-first formal spec.** Not authorized.
- **Paper/shadow planning.** Not authorized.
- **Live-readiness.** Not authorized.
- **Deployment.** Not authorized.
- **Production-key creation.** Forbidden.
- **Exchange-write capability.** Forbidden.
- **MCP / Graphify / `.mcp.json`.** Not enabled.
- **Credentials.** None requested.
- **Authenticated APIs / private endpoints / user stream / WebSocket.** Not used.
- **Data acquisition / patching / regeneration / modification.** No `data/` artefact modified.
- **Forward-fill / interpolation / imputation / replacement.** Not applied.

---

## 14. Ambiguity-log update

GAP-20260424-032 in `docs/00-meta/implementation-ambiguity-log.md` is updated by Phase 3v:

- **Status:** changes from `OPEN` to `RESOLVED`.
- **Operator decision:** records "Resolved by Phase 3v governance memo (2026-04-30): historical backtests remain trade-price-stop-provenance; future runtime/live remains MARK_PRICE-locked; future evidence/runtime artifacts must label stop-trigger domain explicitly; `mixed_or_unknown` fails closed; no verdict revision."
- **Resolution evidence:** points to `docs/00-meta/implementation-reports/2026-04-30_phase-3v_gap-20260424-032-stop-trigger-domain-resolution.md`.

The ambiguity-log update is the only `docs/00-meta/implementation-ambiguity-log.md` modification authorized by Phase 3v.

---

## 15. Forbidden-work confirmation

- **No diagnostics run.** Phase 3v computes nothing. No 5m bar loaded; no statistic computed; no table generated.
- **No Q1–Q7 rerun.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **No data acquisition / download / patch / regeneration / modification.** Phase 3v consulted no Binance endpoint, downloaded nothing, patched nothing.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No strategy / parameter / threshold / project-lock / prior-verdict modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. **§11.6 unchanged. §1.7.3 mark-price-stop lock unchanged.**
- **No verdict revision.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant proposal.**
- **No new strategy candidate proposal.**
- **No Phase 4 / Phase 4a authorization.**
- **No paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription / public endpoints consulted.** Phase 3v performs no network I/O.
- **No secrets requested or stored.**
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No merge to main.**
- **No successor phase started.**

---

## 16. Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized.
- **GAP-20260424-032:** **RESOLVED** by Phase 3v governance memo. No verdict revised; no policy changed; future evidence and runtime artifacts must label stop-trigger domain explicitly; `mixed_or_unknown` fails closed.
- **Pre-coding blockers (3 OPEN remaining after Phase 3v):**
  - GAP-20260424-030 (break-even rule conflict) — MEDIUM risk; OPEN.
  - GAP-20260424-031 (EMA slope wording) — LOW-MEDIUM risk; OPEN.
  - GAP-20260424-033 (stagnation window) — LOW risk; OPEN.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-3v/gap-20260424-032-stop-trigger-domain-resolution` not merged to main; main = origin/main = `4577d750` unchanged.

---

## 17. Operator decision menu

The operator now has GAP-20260424-032 formally resolved in the project record. The next operator decision is operator-driven only.

### 17.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategic pause continues. Phase 3v joins the running record of the post-V1 / post-F1 / post-D1-A / post-5m-research-thread / post-implementation-readiness-review / post-stop-trigger-domain-resolution pause. No subsequent phase authorized.

**Reasoning:**
- Phase 3v's governance value is realized by the memo itself. Future evidence and runtime artifacts are now bound to the §8.4 label scheme regardless of whether any Option B / C / D follows.
- Pausing preserves operator optionality.
- All locks preserved verbatim.

**What this preserves:** Everything in §13 and §16.

**What this rules out:** No Phase 4 / Phase 4a / fresh-hypothesis research / implementation work / paper-shadow / live-readiness / deployment / production-key / exchange-write activity.

### 17.2 Option B — Authorize a docs-only follow-up memo resolving GAP-20260424-030 / 031 / 033 (CONDITIONAL secondary alternative)

**Description:** Authorize a future docs-only memo that resolves the three remaining OPEN ambiguity-log items (break-even rule conflict; EMA slope wording; stagnation window). These are lower risk than GAP-20260424-032 but are still pre-coding blockers per Phase 3u §8.5.

**Phase 3v view:** Acceptable as conditional secondary. Closes the remaining ambiguity-log OPEN items. Useful regardless of subsequent path. Not endorsed over Option A purely because it is incremental docs work.

### 17.3 Option C — Authorize a docs-only Phase 4a safe-slice scoping memo (CONDITIONAL tertiary alternative)

**Description:** Per Phase 3u §16.3 Option C. Authorize a future docs-only memo defining Phase 4a as a strict subset of Phase 4 with explicit anti-live-readiness preconditions.

**Phase 3v view:** Acceptable as conditional tertiary. Phase 3v's §8.4 label scheme would be an in-scope component of Phase 4a if Phase 4a is ever authorized. Not endorsed over Option A or Option B.

### 17.4 Option D — Authorize a future mark-price-stop sensitivity analysis on retained-evidence populations (CONDITIONAL alternative; LOW expected new information)

**Description:** Authorize a future docs-only or analysis phase that produces a `mark_price_backtest_candidate` on the v002-locked retained-evidence trade populations, applying mark-price stop-trigger modeling.

**Phase 3v view:** Phase 3s Q6 already provided per-trade timing-difference statistics. A full mark-price-stop sensitivity backtest would re-evaluate aggregate-level metrics under the mark-price domain. Expected new information is bounded:
- For R3 / R2 / F1, Q6 found < 1 bar mean-lag. Mark-price-domain aggregate metrics would likely be very close to trade-price-domain metrics. Verdict revision is unlikely on cost-sensitivity grounds and forbidden on procedural grounds (Phase 2y §11.3.5).
- For D1-A, Q6 found ~1.3–1.8 5m-bar lag. Mark-price-domain aggregate metrics would differ more, but D1-A's verdict (FRAMEWORK FAIL — cond_i + cond_iv) is unlikely to be revised by stop-trigger-domain alone (cond_i is BTC R MED expR < 0; the trade-vs-mark domain affects exit fills but the entry-evaluation is unchanged at the M2 layer).
- Performing this analysis with full predeclared evidence thresholds would itself require operator-explicit framework-discipline preconditions.

Phase 3v's view: this is acceptable as a conditional alternative if and only if the operator has a specific motivating question that the current evidence does not answer. The Phase 3v rule (§8) makes the procedural framework explicit; the analysis itself is operator-strategic. **Not recommended now.**

### 17.5 Options E–F — NOT RECOMMENDED

- **E — Implementation / Phase 4 (canonical) / paper-shadow / live-readiness / deployment / production-key / exchange-write.** Per Phase 3u §16.5 + Phase 3v §13. Forbidden / not recommended.
- **F — Strategy rescue / new strategy / regime-first formal spec / ML feasibility / new strategy-family discovery.** Per Phase 3t §14.2 + Phase 3u §14. Not recommended.

### 17.6 Recommendation

**Phase 3v recommends Option A (remain paused) as primary.** Option B (resolve remaining OPEN ambiguity-log items via separate docs-only memos) is acceptable as conditional secondary. Option C (Phase 4a safe-slice scoping memo) is acceptable as conditional tertiary subject to Phase 3u §10 prohibitions. Option D (mark-price-stop sensitivity analysis) is conditional but not recommended now (low expected new information; high procedural cost). Options E and F are not recommended.

---

## 18. Next authorization status

**No next phase has been authorized.** Phase 3v authorizes nothing other than producing this resolution memo, the ambiguity-log update marking GAP-20260424-032 RESOLVED, the optional minimal cross-reference update to `docs/07-risk/stop-loss-policy.md` (if needed), and the accompanying closeout artefact. The operator's decision after Phase 3v is operator-driven only.

Selection of any subsequent phase (resolve GAP-20260424-030 / 031 / 033 per Option B; Phase 4a safe-slice scoping memo per Option C; mark-price-stop sensitivity analysis per Option D; Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write per Option E; fresh-hypothesis research / regime-first / ML feasibility per Option F) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). GAP-20260424-032 is now RESOLVED (per Phase 3v). **Recommended state remains paused.**
