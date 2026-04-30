# Phase 3w — Remaining Ambiguity-Log Resolution Memo (docs-only)

**Authority:** GAP-20260424-030 / 031 / 033 (per `docs/00-meta/implementation-ambiguity-log.md`); Phase 2i §1.7.3 project-level locks; Phase 2y §11.3.5 (no post-hoc loosening); Phase 2p §C.1 (R3 baseline-of-record); Phase 2w §16.1 (R2 FAILED — §11.6); Phase 3d-B2 (F1 HARD REJECT); Phase 3j §11.2 (D1-A MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3t (5m research thread closure); Phase 3u §8.5 (pre-coding blocker review); Phase 3v §8 (GAP-20260424-032 stop-trigger domain governance — §8.4 label-scheme + `mixed_or_unknown` fail-closed precedent); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/07-risk/stop-loss-policy.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 3w — Docs-only **remaining ambiguity-log resolution memo.** Resolves the three remaining OPEN ambiguity-log items (GAP-20260424-030 break-even rule conflict; GAP-20260424-031 EMA slope wording ambiguity; GAP-20260424-033 stagnation window) at the governance level using the same Phase 3v §8 pattern (historical provenance preserved; future runtime / paper / live forced to label semantic choice explicitly; `mixed_or_unknown` fails closed; no retained verdict revised; no strategy parameter / threshold / lock changed; no Phase 4 / 4a authorization).

**Branch:** `phase-3w/remaining-ambiguity-log-resolution`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance — all preserved verbatim.

---

## 1. Summary

Phase 3w resolves the three remaining OPEN ambiguity-log items in `docs/00-meta/implementation-ambiguity-log.md`:

- **GAP-20260424-030** — Break-even rule text conflicts with spec Open Question #8 (`+1.5 R` locked vs `+1.5 R / +2.0 R` open). LOW risk. Pre-coding blocker for any future runtime that implements break-even logic.
- **GAP-20260424-031** — EMA slope wording ambiguous: discrete comparison vs fitted slope. LOW-MEDIUM risk (originally MEDIUM in the log; Phase 3u §8.5 revised classification). Pre-coding blocker for any future runtime that re-implements EMA bias.
- **GAP-20260424-033** — Stagnation window not in Open Questions but discussed as metric. LOW risk. Documentation hygiene item; weak pre-coding blocker.

The three resolutions share a common pattern modeled after the Phase 3v §8 stop-trigger-domain governance rule:

1. **Historical retained-evidence backtests retain their original implementation provenance.** No retroactive change.
2. **No retained verdict is revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
3. **Future runtime / paper / live evidence and runtime artifacts must label the relevant semantic choice explicitly.** Each ambiguity gets its own label scheme.
4. **`mixed_or_unknown` semantic interpretation is invalid and fails closed at any decision boundary.** Same fail-closed semantics as Phase 3v §8.4.
5. **Each resolution is governance-only.** No strategy rules added, removed, or changed. No future runtime is authorized.

All three items become **RESOLVED — Phase 3w governance memo (2026-04-30)** in the ambiguity log. After Phase 3w, the ambiguity log has zero OPEN items relevant to Phase 4a / runtime stop-handling / strategy implementation. Three pre-Phase-3o-era items remain `ACCEPTED_LIMITATION` or `DEFERRED` and are pre-tiny-live concerns rather than pre-coding blockers (per Phase 3u §8.2 / §8.3).

**Phase 3w recommends remain paused as primary.** Phase 4 (canonical) remains unauthorized. Phase 4a (safe slice) remains conditional only and not authorized. The four Phase 3u §8.5 currently-OPEN pre-coding blockers are now all RESOLVED at the governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w).

---

## 2. Authority and boundary

Phase 3w operates strictly inside the post-Phase-3v boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 Phase 4 / 4a prohibitions; Phase 3v §8 stop-trigger-domain governance.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (mark-price stops; one-position max; 0.25% risk; 2× leverage cap; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.

Phase 3w writes *governance language* into the project record and edits *only* the relevant ambiguity-log entries. Phase 3w does NOT modify strategy specs, backtest plans, validation checklists, stop-loss policy, runtime architecture, or any other substantive document. Phase 3w does NOT write code, run diagnostics, or run backtests. Phase 3w does NOT authorize Phase 4 / 4a / paper-shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials.

---

## 3. Starting state

```text
branch:           phase-3w/remaining-ambiguity-log-resolution
parent commit:    fdbbfabfc935fb9dfb521250d3dcb4e711216be6 (post-Phase-3v-merge housekeeping)
working tree:     clean
main:             fdbbfabfc935fb9dfb521250d3dcb4e711216be6 (unchanged)

ambiguity-log OPEN items (pre-Phase-3w):
  - GAP-20260424-030 (LOW risk; break-even rule text conflict).
  - GAP-20260424-031 (LOW-MEDIUM risk per Phase 3u §8.5; EMA slope wording).
  - GAP-20260424-033 (LOW risk; stagnation window).

ambiguity-log RESOLVED / ACCEPTED_LIMITATION / DEFERRED items:
  - GAP-20260424-032 RESOLVED by Phase 3v §8.
  - All other Phase-1 / Phase-2 GAP entries RESOLVED, ACCEPTED_LIMITATION, or DEFERRED.

phase-gate state: Phase 4 unauthorized; Phase 4a conditional only.
research thread:  5m research thread operationally complete (Phase 3t).
v002 datasets:    locked; manifests untouched.
Phase 3q v001-of-5m manifests: trade-price research-eligible; mark-price research_eligible:false.
locks:            §11.6 = 8 bps HIGH per side; §1.7.3 mark-price stops; preserved.
```

---

## 4. Ambiguities being resolved

### 4.1 GAP-20260424-030 — Break-even rule text conflicts with spec Open Question #8

Per `docs/00-meta/implementation-ambiguity-log.md` (lines 827–854):

- **Spec assertion (line 380):** Stage-4 break-even rule = "when the trade reaches +1.5 R MFE, move the stop to break-even".
- **Spec Open Questions (line 564):** Open Question #8 = "Should the break-even transition happen at +1.5 R or +2.0 R?".
- **Internal inconsistency:** the same value is treated as both a locked rule (line 380) and an open research question (line 564).
- **Phase 2f resolution stance:** Option C (defer; treat the value as parametric per Open Q #8; H-D3 wave-1 variant tested +2.0 R).

### 4.2 GAP-20260424-031 — EMA slope wording ambiguous

Per `docs/00-meta/implementation-ambiguity-log.md` (lines 858–885):

- **Spec wording (lines 156–172):** Long bias = "1h EMA(50) is rising versus 3 completed 1h candles earlier"; short bias = "1h EMA(50) is falling versus 3 completed 1h candles earlier".
- **Two valid interpretations:**
  - Discrete comparison: `EMA[now] > EMA[now − 3h]`.
  - Fitted slope: e.g., linear regression slope over last 3 (or 4) completed 1h bars.
- **Phase 2f resolution stance:** Option C (defer; record discrete-comparison as the working implementation convention; require any HTF-bias variant to explicitly specify in its Gate 1 plan).

### 4.3 GAP-20260424-033 — Stagnation window not in Open Questions

Per `docs/00-meta/implementation-ambiguity-log.md` (lines 920–946):

- **Spec assertion (line 415):** Stagnation exit = "if, after 8 completed 15m bars from entry, the trade has not reached at least +1.0 R MFE, exit at market".
- **Backtest plan treatment:** "stagnation-exit frequency" is a trade-quality metric to review (implying the value may be revisable).
- **Internal tension:** the rule is locked in the spec but the backtest plan treats its value as evidence-revisable.
- **Phase 2f resolution stance:** Option C (defer; classify as parametric; flag for operator confirmation before any wave that includes H-D5 stagnation-window variant).

---

## 5. Resolution principles

Phase 3w applies the following principles, modeled after Phase 3v §8 stop-trigger-domain governance:

### 5.1 Historical retained-evidence verdicts remain unchanged

R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. **Preserved verbatim.** No retained verdict is reopened by Phase 3w.

### 5.2 Historical backtest behavior preserved under its original implementation provenance

Each retained-evidence backtest ran under a specific, executed implementation convention. Phase 3w records that convention as the canonical historical provenance for that backtest, without revising the verdict and without modifying the spec text retroactively.

### 5.3 Executed backtest behavior is canonical historical provenance

If executed code unambiguously implemented a specific convention, Phase 3w records that convention without revising verdicts. The spec text may remain ambiguous; the executed convention takes precedence as historical evidence.

### 5.4 Text conflicts resolved as future-implementation guardrails

Where spec text conflicts cannot be resolved without changing strategy behavior, Phase 3w records the conflict as a future-implementation guardrail (a labeled choice that future runtime must declare) rather than as a retroactive strategy change. **No retained verdict is revised by this guardrail.**

### 5.5 Future implementation artifacts must make the relevant semantic choice explicit

Each resolution defines a label scheme analogous to Phase 3v §8.4. Future evidence and runtime artifacts must declare the semantic choice explicitly.

### 5.6 Unknown or mixed semantic interpretation fails closed

Same fail-closed semantics as Phase 3v §8.4. A `mixed_or_unknown` value at any decision boundary must block the trade / verdict / persist / promotion.

### 5.7 No revision of strategy parameters / thresholds / locks / verdicts

Phase 3w does NOT change R3 / R2 / F1 / D1-A / H0 / R1a / R1b-narrow specs or verdicts. Phase 3w does NOT change §10.3 / §10.4 / §11.3 / §11.4 / §11.6. Phase 3w does NOT change §1.7.3.

### 5.8 No authorization of Phase 4 / 4a / paper-shadow / live-readiness / deployment / credentials / exchange-write

Phase 3w is governance-only. No subsequent phase is authorized.

---

## 6. GAP-20260424-030 resolution

### 6.1 Historical break-even-rule provenance (canonical)

The break-even rule (Stage-4 of staged-trailing exit) was implemented and applied as follows in the retained-evidence trade populations:

| Candidate | Exit-management family | Break-even rule status | Canonical provenance label |
|---|---|---|---|
| **H0** (Phase 2e baseline) | Staged-trailing exit | **Active** at `+1.5 R MFE → move stop to break-even` per spec line 380. | `break_even_rule = enabled_plus_1_5R_mfe` |
| **R1a** (volatility-percentile setup; Phase 2m) | Inherits H0 staged-trailing exit | **Active** (same as H0). | `break_even_rule = enabled_plus_1_5R_mfe` |
| **R1b-narrow** (bias-strength setup; Phase 2s) | Inherits H0 staged-trailing exit | **Active** (same as H0). | `break_even_rule = enabled_plus_1_5R_mfe` |
| **R2** (pullback-retest entry; Phase 2w) | Inherits H0 staged-trailing exit (entry-axis variant only) | **Active** (same as H0). | `break_even_rule = enabled_plus_1_5R_mfe` |
| **R3** (Fixed-R + 8-bar time-stop, baseline-of-record per Phase 2p §C.1) | Replaced staged-trailing with Fixed-R + unconditional time-stop | **Not active.** R3 explicitly removed staged-trailing; break-even step is structurally absent. | `break_even_rule = disabled` |
| **F1** (mean-reversion-after-overextension; Phase 3d-B2) | Independent exit family (8-bar cumulative-displacement target + structural stop + 8-bar time-stop) | **Not active.** F1 has no staged-trailing. | `break_even_rule = disabled` |
| **D1-A** (funding-aware contrarian; Phase 3j) | Independent exit family (Fixed-R target + 32-bar time-stop) | **Not active.** D1-A has no staged-trailing. | `break_even_rule = disabled` |

The H-D3 wave-1 variant in Phase 2g tested `break_even_rule = enabled_plus_2_0R_mfe` as a parametric variant of the H0 exit family. Per the retained-evidence record (Phase 2g wave-1), H-D3 did not produce a candidate that was promoted forward; the staged-trailing exit family was superseded by R3's Fixed-R + time-stop redesign in Phase 2p.

### 6.2 Resolution

**GAP-20260424-030 is RESOLVED — Phase 3w governance memo (2026-04-30).**

1. **Historical verdicts preserved verbatim.** No retained-evidence candidate is reopened by Phase 3w. The break-even rule's canonical historical provenance is recorded per §6.1 above.
2. **No retroactive spec edit.** The spec text at `docs/03-strategy-research/v1-breakout-strategy-spec.md` lines 380 and 564 is NOT modified by Phase 3w. The internal inconsistency (locked rule vs Open Question #8) is now resolved at the governance level via the §6.3 future-runtime guardrail rather than via spec edit.
3. **No break-even behavior is added, removed, or changed.** R3's `break_even_rule = disabled` and H0 / R1a / R1b-narrow / R2's `break_even_rule = enabled_plus_1_5R_mfe` provenance is preserved.

### 6.3 Required future-runtime guardrail

If any future runtime / paper / live phase ever implements break-even logic (and Phase 3w does NOT authorize any such phase), the runtime must declare a `break_even_rule` label as a first-class config / persistence field. Valid values:

- **`disabled`** — no break-even step (R3 / F1 / D1-A historical provenance).
- **`enabled_plus_1_5R_mfe`** — staged-trailing Stage-4 break-even at `+1.5 R MFE` (H0 / R1a / R1b-narrow / R2 historical provenance per spec line 380).
- **`enabled_plus_2_0R_mfe`** — staged-trailing Stage-4 break-even at `+2.0 R MFE` (H-D3 wave-1 variant provenance; not a retained-evidence verdict).
- **`enabled_<other_predeclared>`** — any other predeclared break-even rule with explicit MFE threshold and explicit predeclared evidence threshold for its evaluation.
- **`mixed_or_unknown`** — **invalid**. Fails closed at any decision boundary (block trade / block verdict / block persist / block evidence-promotion).

The label requirement is binding from the Phase 3w commit forward on any future evidence or runtime artifact that handles break-even logic.

### 6.4 What Phase 3w does not do

- Phase 3w does NOT add, remove, or change any break-even rule.
- Phase 3w does NOT revise R3 / R2 / F1 / D1-A / H0 / R1a / R1b-narrow verdicts.
- Phase 3w does NOT modify `docs/03-strategy-research/v1-breakout-strategy-spec.md` lines 380 or 564.
- Phase 3w does NOT authorize a future H-D3-style break-even variant phase.
- Phase 3w does NOT propose any strategy successor.
- Phase 3w does NOT authorize Phase 4 / 4a / paper-shadow / live-readiness / deployment.

---

## 7. GAP-20260424-031 resolution

### 7.1 Historical EMA-slope provenance (canonical)

The 1h EMA(50) slope rule was implemented as the discrete-comparison interpretation in the retained-evidence trade populations:

- **Convention:** `EMA[now] > EMA[now − 3h]` for long bias; `EMA[now] < EMA[now − 3h]` for short bias.
- **Reference points:** the latest completed 1h bar's EMA(50) value is compared to the EMA(50) value of the bar 3 completed 1h bars earlier.
- **Phase 2f memo confirmation:** the working implementation convention is discrete comparison.

| Candidate | Exit / entry family | EMA-slope-method | Canonical provenance label |
|---|---|---|---|
| H0 | V1 breakout | discrete comparison | `ema_slope_method = discrete_comparison` |
| R1a | V1 breakout (volatility-percentile setup variant) | discrete comparison (inherited) | `ema_slope_method = discrete_comparison` |
| R1b-narrow | V1 breakout (bias-strength setup variant) | discrete comparison (inherited) | `ema_slope_method = discrete_comparison` |
| R2 | V1 breakout (pullback-retest entry variant) | discrete comparison (inherited) | `ema_slope_method = discrete_comparison` |
| R3 | V1 breakout (Fixed-R + 8-bar time-stop exit redesign) | discrete comparison (inherited; entry side unchanged) | `ema_slope_method = discrete_comparison` |
| F1 | Mean-reversion (independent strategy family) | not applicable (F1 does not use 1h EMA bias as primary entry filter) | `ema_slope_method = not_applicable` |
| D1-A | Funding-aware contrarian (independent strategy family) | not applicable (D1-A does not use 1h EMA bias as primary entry filter) | `ema_slope_method = not_applicable` |

Variant H-C1 in the Phase 2f memo tested a different EMA *pair* (20/100) but preserved the discrete-comparison interpretation. No fitted-slope variant H-C2 has been run; no fitted-slope evidence exists in the retained-evidence record.

### 7.2 Resolution

**GAP-20260424-031 is RESOLVED — Phase 3w governance memo (2026-04-30).**

1. **Historical verdicts preserved verbatim.** No retained-evidence candidate is reopened by Phase 3w. The EMA-slope-method canonical historical provenance is recorded per §7.1 above.
2. **No retroactive spec edit.** The spec text at `docs/03-strategy-research/v1-breakout-strategy-spec.md` lines 156–172 is NOT modified by Phase 3w. The wording ambiguity is resolved at the governance level via the §7.3 future-runtime guardrail.
3. **No EMA logic is changed.** All retained-evidence backtests continue to be canonically attributed to `ema_slope_method = discrete_comparison`.

### 7.3 Required future-runtime guardrail

If any future runtime / paper / live phase or any future research backtest ever implements 1h EMA bias logic (and Phase 3w does NOT authorize any such phase), the runtime / backtest must declare an `ema_slope_method` label as a first-class config / persistence field. Valid values:

- **`discrete_comparison`** — `EMA[now] > EMA[now − 3h]` (long); `EMA[now] < EMA[now − 3h]` (short). Canonical historical provenance for V1 family retained-evidence backtests.
- **`fitted_slope`** — a regression-fit slope over the last N completed 1h bars, with N predeclared (e.g., N=3 or N=4). Not used by any retained-evidence backtest; would constitute a separately predeclared hypothesis (analogous to a future H-C2 variant).
- **`other_predeclared`** — any other predeclared method with explicit specification and explicit predeclared evaluation threshold.
- **`not_applicable`** — for strategy families that do not use 1h EMA bias as primary entry filter (F1 / D1-A historical provenance).
- **`mixed_or_unknown`** — **invalid**. Fails closed at any decision boundary.

The label requirement is binding from the Phase 3w commit forward.

### 7.4 What Phase 3w does not do

- Phase 3w does NOT change the EMA logic.
- Phase 3w does NOT reclassify any retained-evidence verdict.
- Phase 3w does NOT modify spec lines 156–172.
- Phase 3w does NOT authorize a fitted-slope H-C2-style variant phase.
- Phase 3w does NOT authorize Phase 4 / 4a / paper-shadow / live-readiness / deployment.

---

## 8. GAP-20260424-033 resolution

### 8.1 Historical stagnation-window provenance (canonical)

The stagnation rule (line 415: "if, after 8 completed 15m bars from entry, the trade has not reached at least +1.0 R MFE, exit at market") was implemented as follows in the retained-evidence trade populations:

| Candidate | Exit family | Stagnation-window role | Canonical provenance label |
|---|---|---|---|
| **H0** (Phase 2e baseline) | Staged-trailing exit | **Active rule** at `8 bars / +1.0 R MFE → exit at market`. | `stagnation_window_role = active_rule_predeclared` |
| **R1a** | Inherits H0 staged-trailing | **Active rule** (same as H0). | `stagnation_window_role = active_rule_predeclared` |
| **R1b-narrow** | Inherits H0 staged-trailing | **Active rule** (same as H0). | `stagnation_window_role = active_rule_predeclared` |
| **R2** | Inherits H0 staged-trailing | **Active rule** (same as H0). | `stagnation_window_role = active_rule_predeclared` |
| **R3** (baseline-of-record; Fixed-R + unconditional 8-bar time-stop) | Replaced staged-trailing with Fixed-R + 8-bar time-stop | **Not active as stagnation.** R3's 8-bar exit fires *unconditionally* at 8 bars regardless of MFE; this is structurally different from H0's stagnation rule (which fires at 8 bars *only if* MFE < +1.0 R). | `stagnation_window_role = not_active` |
| **F1** | Independent exit family (8-bar cumulative-displacement target + structural stop + 8-bar unconditional time-stop) | **Not active as stagnation.** F1's 8-bar time-stop fires unconditionally; not gated on MFE. | `stagnation_window_role = not_active` |
| **D1-A** | Independent exit family (Fixed-R target + 32-bar unconditional time-stop) | **Not active as stagnation.** D1-A's 32-bar time-stop fires unconditionally; not gated on MFE. | `stagnation_window_role = not_active` |

Variant H-D5 (stagnation-window 6/10/12 bars) was deferred per the original ambiguity-log entry; no retained-evidence record contains an H-D5 result. Phase 3w does not propose H-D5 or any successor.

The backtest plan's treatment of "stagnation-exit frequency" as a trade-quality metric is a *metric-only* convention — i.e., the metric is reported in evaluation reports for trades whose exit reason was the stagnation rule. The metric itself is descriptive and does not constitute a rule change.

### 8.2 Resolution

**GAP-20260424-033 is RESOLVED — Phase 3w governance memo (2026-04-30).**

1. **Historical verdicts preserved verbatim.** No retained-evidence candidate is reopened by Phase 3w. The stagnation-window-role canonical historical provenance is recorded per §8.1 above.
2. **No retroactive spec edit.** The spec text at `docs/03-strategy-research/v1-breakout-strategy-spec.md` line 415 is NOT modified by Phase 3w. The Open-Questions-section silence is resolved at the governance level via the §8.3 future-runtime guardrail.
3. **No stagnation rule is added, removed, or changed.** H0 / R1a / R1b-narrow / R2's `stagnation_window_role = active_rule_predeclared` and R3 / F1 / D1-A's `stagnation_window_role = not_active` provenance are preserved.

### 8.3 Required future-runtime guardrail

If any future runtime / paper / live phase or any future research backtest ever uses stagnation logic in any role (and Phase 3w does NOT authorize any such phase), the runtime / backtest must declare a `stagnation_window_role` label as a first-class config / persistence field. Valid values:

- **`not_active`** — no stagnation rule applied. Canonical provenance for R3 / F1 / D1-A.
- **`metric_only`** — stagnation is observed and reported as a trade-quality metric but does NOT alter exit behavior. The backtest-plan-mentioned "stagnation-exit frequency" framing falls under this label *only if* the stagnation rule itself is `not_active` — i.e., a `metric_only` label cannot be used to silently re-introduce an active stagnation rule.
- **`active_rule_predeclared`** — stagnation rule is active with a predeclared `stagnation_bars` and `stagnation_min_mfe_R` configuration. The default historical convention is `stagnation_bars = 8`, `stagnation_min_mfe_R = +1.0 R`. Canonical provenance for H0 / R1a / R1b-narrow / R2.
- **`mixed_or_unknown`** — **invalid**. Fails closed at any decision boundary.

The label requirement is binding from the Phase 3w commit forward.

### 8.4 What Phase 3w does not do

- Phase 3w does NOT add, remove, or change any stagnation rule.
- Phase 3w does NOT add stagnation as an exit, filter, metric, or rule to any candidate that did not have it (R3 / F1 / D1-A still `not_active`).
- Phase 3w does NOT remove stagnation from any candidate that had it (H0 / R1a / R1b-narrow / R2 still `active_rule_predeclared`).
- Phase 3w does NOT modify spec line 415 or the backtest plan §Metrics — stagnation-exit frequency.
- Phase 3w does NOT authorize an H-D5-style stagnation-window variant phase.
- Phase 3w does NOT authorize Phase 4 / 4a / paper-shadow / live-readiness / deployment.

---

## 9. Required future artifact labels or disclosures

Combining §6.3 + §7.3 + §8.3 with Phase 3v §8.4, future evidence and runtime artifacts must carry the following first-class labels (where the relevant logic exists):

| Label | Valid values | Fail-closed value |
|---|---|---|
| `stop_trigger_domain` (Phase 3v §8.4) | `trade_price_backtest` \| `mark_price_runtime` \| `mark_price_backtest_candidate` | `mixed_or_unknown` |
| `break_even_rule` (Phase 3w §6.3) | `disabled` \| `enabled_plus_1_5R_mfe` \| `enabled_plus_2_0R_mfe` \| `enabled_<other_predeclared>` | `mixed_or_unknown` |
| `ema_slope_method` (Phase 3w §7.3) | `discrete_comparison` \| `fitted_slope` \| `other_predeclared` \| `not_applicable` | `mixed_or_unknown` |
| `stagnation_window_role` (Phase 3w §8.3) | `not_active` \| `metric_only` \| `active_rule_predeclared` | `mixed_or_unknown` |

Future artifacts in scope:

- Backtest report manifests (`backtest_report.manifest.json` `config_snapshot`).
- Runtime persistence schemas (per `docs/08-architecture/runtime-persistence-spec.md` for any future runtime).
- Runtime event contracts (per `docs/08-architecture/internal-event-contracts.md` for any future runtime).
- Dashboard read models (per `docs/11-interface/operator-dashboard-requirements.md` for any future runtime).
- Trade-execution decisions (any future runtime).
- Risk-engine validations (any future runtime).
- Operator-facing alert messages (any future runtime).
- Any future research backtest output report.

Existing artefacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs) are NOT retroactively modified by Phase 3w. The label requirement applies prospectively to any new artefact created from the Phase 3w commit forward.

For audit purposes, existing Phase 2 / Phase 3 retained-evidence backtest reports should be treated as having the *implicit* labels recorded in §6.1 / §7.1 / §8.1 above (consistent with their actual implementation provenance). This implicit-label convention is documentary only; no manifest is rewritten.

---

## 10. Implications for retained verdicts

Phase 3w preserves all retained-evidence verdicts verbatim:

| Candidate | Verdict | Phase 3w action |
|---|---|---|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1 | **Preserved verbatim.** Implicit labels: `stop_trigger_domain = trade_price_backtest`; `break_even_rule = disabled`; `ema_slope_method = discrete_comparison`; `stagnation_window_role = not_active`. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3 | **Preserved verbatim.** Implicit labels: `stop_trigger_domain = trade_price_backtest`; `break_even_rule = enabled_plus_1_5R_mfe`; `ema_slope_method = discrete_comparison`; `stagnation_window_role = active_rule_predeclared`. |
| **R1a** | Retained research evidence only; non-leading | **Preserved verbatim.** Same implicit labels as H0. |
| **R1b-narrow** | Retained research evidence only; non-leading | **Preserved verbatim.** Same implicit labels as H0. |
| **R2** | FAILED — §11.6 cost-sensitivity blocks per Phase 2w §16.1 | **Preserved verbatim.** Same implicit labels as H0. |
| **F1** | HARD REJECT per Phase 3c §7.3; Phase 3d-B2 terminal | **Preserved verbatim.** Implicit labels: `stop_trigger_domain = trade_price_backtest`; `break_even_rule = disabled`; `ema_slope_method = not_applicable`; `stagnation_window_role = not_active`. |
| **D1-A** | MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2; Phase 3j terminal | **Preserved verbatim.** Same implicit labels as F1. |

**No retained-evidence verdict is reopened, revised, weakened, or strengthened by Phase 3w.** Phase 3w is a procedural / governance memo, not a verdict-revision phase.

---

## 11. Implications for future backtests

If the operator ever authorizes a future backtest phase, the Phase 3w resolutions plus the Phase 3v §8.4 stop-trigger-domain rule require:

### 11.1 All four labels must be predeclared in the phase brief

Any future backtest phase brief must explicitly declare:
- `stop_trigger_domain` (per Phase 3v §8.4).
- `break_even_rule` (per Phase 3w §6.3).
- `ema_slope_method` (per Phase 3w §7.3).
- `stagnation_window_role` (per Phase 3w §8.3).

### 11.2 No silent label drift

A backtest cannot declare one label set in its brief and produce evidence under a different label set. Silent drift fails closed at the evidence-promotion boundary.

### 11.3 Cross-domain comparability is bounded

A backtest with a different label set than a retained-evidence backtest cannot be directly compared verdict-for-verdict without explicit caveats. Cross-domain comparison must explicitly call out the differing labels and apply Phase 2f Gate 1 / §11.3 / §11.6 framework discipline separately.

### 11.4 Live-readiness disclosures (Phase 3v §8.5 + Phase 3w extension)

Any future backtest intended to support paper/shadow/live-readiness claims must:
- Use `stop_trigger_domain = mark_price_backtest_candidate` per Phase 3v §8.5.
- Declare `break_even_rule`, `ema_slope_method`, and `stagnation_window_role` consistent with the future runtime that the backtest is meant to validate.
- Or explicitly disclose that it is not live-readiness evidence.

### 11.5 Phase 3w does not authorize any future backtest

The above are *prospective rules*. Phase 3w itself does NOT authorize any future backtest, mark-price sensitivity analysis, EMA-slope sensitivity analysis, stagnation-window sensitivity analysis, break-even-rule sensitivity analysis, or re-evaluation of retained-evidence populations.

---

## 12. Implications for future Phase 4a / runtime work

If a future Phase 4a (or any subsequent runtime phase) is ever authorized (and Phase 3w does NOT authorize Phase 4a), the Phase 3w resolutions plus Phase 3v §8 require:

### 12.1 Label enforcement at runtime

Any runtime code path that touches break-even logic, EMA-bias logic, stagnation logic, or stop-trigger logic must:
- Tag every relevant event / state / decision with the appropriate label per §9 above.
- Reject any event / state / decision that cannot be unambiguously labeled (`mixed_or_unknown` → fail closed).
- Persist label values as first-class fields per `docs/08-architecture/runtime-persistence-spec.md` for any future runtime.

### 12.2 Backtest-vs-runtime consistency check

A runtime that consumes backtest verdicts as inputs (e.g., a strategy-readiness gate) must check that the source backtest's label set matches the runtime's expected label set:
- Stop-trigger domain match per Phase 3v §8.5.
- Break-even rule match per Phase 3w §6.3.
- EMA slope method match per Phase 3w §7.3.
- Stagnation window role match per Phase 3w §8.3.

A label mismatch fails closed at the readiness-gate boundary.

### 12.3 Phase 4a prohibition list (preserved from Phase 3u §10 + Phase 3v §8.7)

Phase 4a, if ever authorized, must NOT:
- Place orders.
- Implement exchange-write capability.
- Use production keys, authenticated APIs, private endpoints, user stream, or WebSocket.
- Enable MCP / Graphify / `.mcp.json`.
- Propose strategy rescue or new strategy candidates.
- Relax §1.7.3, §10.3 / §10.4 / §11.3 / §11.4 / §11.6, mark-price-stop lock, or any other lock.
- Imply paper/shadow / live-readiness / deployment / production-key / exchange-write authorization.
- Modify, remove, or relax the Phase 3v §8 or Phase 3w §6 / §7 / §8 governance rules.

### 12.4 Phase 3w does not authorize Phase 4a

The above are *prospective rules*. Phase 3w itself does NOT authorize Phase 4a, runtime implementation, or any code change.

---

## 13. Ambiguity-log update

`docs/00-meta/implementation-ambiguity-log.md` is updated by Phase 3w to mark the three OPEN entries RESOLVED:

- **GAP-20260424-030** — Status changes from `OPEN` to `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records the §6 resolution. Resolution evidence points to the Phase 3w memo.
- **GAP-20260424-031** — Status changes from `OPEN` to `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records the §7 resolution. Resolution evidence points to the Phase 3w memo.
- **GAP-20260424-033** — Status changes from `OPEN` to `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records the §8 resolution. Resolution evidence points to the Phase 3w memo.

The ambiguity-log update is the only `docs/00-meta/implementation-ambiguity-log.md` modification authorized by Phase 3w.

---

## 14. What this does not authorize

Phase 3w explicitly does NOT authorize, propose, or initiate any of the following:

- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **Threshold revision.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 preserved verbatim.
- **Project-lock revision.** §1.7.3 preserved verbatim.
- **Strategy-parameter revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A specs preserved verbatim.
- **Strategy rescue.** No R2 / F1 / D1-A successor authorized.
- **5m strategy / hybrid / variant.** Phase 3o §4.1 / Phase 3p §10 prohibition preserved.
- **New strategy candidate.** Phase 3t §14.2 / Phase 3u §14 fresh-hypothesis-research-paused recommendation stands.
- **Phase 4 / Phase 4a authorization.** Phase 3u §16 + Phase 3v §17 recommendations stand.
- **Backtest re-running.** No future backtest authorized by Phase 3w. H-D3 / H-C2 / H-D5 sensitivity analyses NOT authorized.
- **Manifest re-issue.** All `data/manifests/*.manifest.json` files preserved verbatim. Mark-price 5m `research_eligible: false` flag preserved.
- **Spec / backtest-plan / validation-checklist edit.** Substantive content preserved verbatim. Phase 3w writes governance language into the project record via the resolution memo + ambiguity-log entries; it does NOT rewrite specs.
- **Phase 3p §4.7 amendment.** Preserved verbatim.
- **Phase 3v §8 amendment.** Preserved verbatim.
- **Phase 3o / 3p / 3r / 3s / 3t / 3u / 3v rule modification.** All preserved.
- **Implementation.** No runtime / strategy / execution / risk-engine / database / dashboard / observability / test code changed.
- **Backtests.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
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

## 15. Forbidden-work confirmation

- **No diagnostics run.** Phase 3w computes nothing.
- **No Q1–Q7 rerun.**
- **No backtests run.**
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No strategy / parameter / threshold / project-lock / prior-verdict modification.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim.
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved.
- **No 5m strategy / hybrid / retained-evidence successor / new variant proposal.**
- **No new strategy candidate proposal.**
- **No Phase 4 / Phase 4a authorization.**
- **No paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription / public endpoints consulted.** Phase 3w performs no network I/O.
- **No secrets requested or stored.**
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No spec / backtest-plan / validation-checklist substantive edit.**
- **No Phase 3v §8 stop-trigger-domain rule modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 16. Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8.
- **Break-even rule governance:** RESOLVED by Phase 3w §6.
- **EMA slope method governance:** RESOLVED by Phase 3w §7.
- **Stagnation window role governance:** RESOLVED by Phase 3w §8.
- **OPEN ambiguity-log items after Phase 3w:** zero relevant to Phase 4a / runtime / strategy implementation. Pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED`) remain as documented in the ambiguity log and `docs/12-roadmap/technical-debt-register.md` (e.g., GAP-20260419-018 taker commission rate parameterization; GAP-20260419-020 ExchangeInfo snapshot proxy; GAP-20260419-024 leverageBracket placeholder; GAP-20260419-025 wider historical backfill DEFERRED). These are pre-tiny-live concerns, not pre-coding blockers.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-3w/remaining-ambiguity-log-resolution` not merged to main; main = origin/main = `fdbbfab` unchanged.

---

## 17. Operator decision menu

The operator now has all four Phase 3u §8.5 currently-OPEN pre-coding blockers RESOLVED at the governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w). The next operator decision is operator-driven only.

### 17.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. Phase 3w joins the running record. No subsequent phase authorized.

**Reasoning:**
- All four pre-coding blockers (GAP-20260424-030 / 031 / 032 / 033) are now RESOLVED at the governance level.
- The four label schemes (`stop_trigger_domain`, `break_even_rule`, `ema_slope_method`, `stagnation_window_role`) are binding from Phase 3w forward on any future evidence or runtime artefact. Their value is realized regardless of any subsequent phase.
- Pausing preserves operator optionality.

**What this preserves:** All locks, all verdicts, all Phase 3o–3v predeclaration discipline, all four governance label schemes.

**What this rules out:** No Phase 4 / Phase 4a / fresh-hypothesis research / implementation / paper-shadow / live-readiness / deployment / production-key / exchange-write activity.

### 17.2 Option B — Authorize a docs-only Phase 4a safe-slice scoping memo (CONDITIONAL secondary alternative)

**Description:** Per Phase 3u §16.3 / Phase 3v §17.3. Authorize a docs-only memo defining Phase 4a as a strict subset of Phase 4 with explicit anti-live-readiness preconditions. Phase 4a, if later authorized for execution, would inherit the four governance label schemes (Phase 3v §8 + Phase 3w §6 / §7 / §8).

**Phase 3w view:** Acceptable as conditional secondary. Phase 3w resolves the last governance pre-blockers; Option B becomes more procedurally well-grounded after Phase 3w. Still not endorsed over Option A; the operator should be willing to commit to deprioritize research in writing before authorizing Option B.

### 17.3 Option C — Authorize sensitivity analyses (mark-price stop / fitted-slope / break-even / stagnation) on retained-evidence populations (CONDITIONAL alternative; LOW expected new information)

**Description:** Authorize a future backtest phase that runs one or more of: H-D3 break-even +2.0R variant; H-C2 fitted-slope EMA variant; H-D5 stagnation-window 6/10/12 bars; mark-price stop sensitivity. All would be `mark_price_backtest_candidate` or `trade_price_backtest` per Phase 3v §8.5.

**Phase 3w view:** Same posture as Phase 3v §17.4. Bounded marginal information value. Procedurally heavy. **Not recommended now.**

### 17.4 Option D — Authorize fresh-hypothesis research (NOT RECOMMENDED NOW)

Per Phase 3t §14.2 / Phase 3u §14 / Phase 3v §17.

### 17.5 Option E — Phase 4 (canonical) / paper-shadow / live-readiness / deployment / production-key / exchange-write (FORBIDDEN / NOT RECOMMENDED)

Per Phase 3u §16.5 / Phase 3v §17.5.

### 17.6 Recommendation

**Phase 3w recommends Option A (remain paused) as primary.** Option B (docs-only Phase 4a safe-slice scoping memo) is acceptable as conditional secondary. Option C is conditional but not recommended now. Options D and E are not recommended.

---

## 18. Next authorization status

**No next phase has been authorized.** Phase 3w authorizes nothing other than producing this resolution memo, the ambiguity-log update marking GAP-20260424-030 / 031 / 033 RESOLVED, and the accompanying closeout artefact. The operator's decision after Phase 3w is operator-driven only.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 currently-OPEN pre-coding blockers (GAP-20260424-030 / 031 / 032 / 033) are now RESOLVED at the governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w). **Recommended state remains paused.**
