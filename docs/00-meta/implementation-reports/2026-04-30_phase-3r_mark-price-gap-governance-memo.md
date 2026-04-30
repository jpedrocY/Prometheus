# Phase 3r — Mark-Price Gap Governance Memo (docs-only)

**Authority:** Phase 3p §4.7 / §6.2 (strict integrity-check evidence specification); Phase 3p §10 Option B (conditional secondary alternative — *docs-only governance memo formalizing the mark-price gap-handling decision before any potential Q1–Q7 diagnostics-execution*); Phase 3q evidence (`docs/00-meta/implementation-reports/2026-04-30_phase-3q_5m-data-acquisition-and-integrity-validation.md`, `docs/00-meta/implementation-reports/2026-04-30_phase-3q_closeout.md`); Phase 3o §6 (forbidden question forms) + §10 (allowed-vs-forbidden analysis boundary); `docs/04-data/data-requirements.md` (forbidden-patterns: no forward-fill, no silent gap omission); `docs/04-data/dataset-versioning.md` (immutability + manifest policy); `docs/04-data/timestamp-policy.md` (UTC ms canonical); `docs/04-data/historical-data-spec.md` (Binance public bulk-archive convention); Phase 2y §11.3.5 (no post-hoc loosening); Phase 2i §1.7.3 (project-level locks); `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-mcp-and-secrets.md`; `.claude/rules/prometheus-safety.md`.

**Phase:** 3r — Docs-only **mark-price gap governance memo.** Formalizes the governance handling for the four upstream `data.binance.vision` maintenance-window gaps that Phase 3q surfaced in the 5m mark-price supplemental datasets. Operator selected Option B from Phase 3p §10 / Phase 3q decision menu: a docs-only governance decision *before* any potential Q1–Q7 diagnostics-execution phase. Phase 3r is purely a written governance artefact; it acquires no data, runs no diagnostics, answers no Q1–Q7, modifies no datasets / manifests / strategy specs / thresholds / project-locks / prior verdicts, and authorizes no successor phase.

**Branch:** `phase-3r/mark-price-gap-governance`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim. **No code change. No data acquisition. No data modification. No diagnostics. No backtests. No prior-verdict revision. No project-lock revision. No threshold revision. No strategy-parameter change. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work proposed.** Recommendation is provisional and evidence-based; the operator decides.

---

## 1. Summary

Phase 3q (docs-and-data) acquired four supplemental v001-of-5m datasets (`binance_usdm_btcusdt_5m__v001`, `binance_usdm_ethusdt_5m__v001`, `binance_usdm_btcusdt_markprice_5m__v001`, `binance_usdm_ethusdt_markprice_5m__v001`). The two trade-price datasets passed Phase 3p §4.7 strict integrity gate. The two mark-price datasets each failed the gap-zero clause due to four upstream `data.binance.vision` maintenance-window gaps (BTC: 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10). The same gap pattern is verified to be present in the locked v002 mark-price 15m datasets, where the v002 manifest's `invalid_windows: []` was technically inaccurate but was accepted in the retained-evidence trade-population provenance trail.

This is a real governance question — not a strategy or research question. The brief's failure-path required Phase 3q to stop for operator review. The operator selected Phase 3p §10 Option B: write a docs-only governance memo that decides, *before any diagnostics-execution phase is even authorized*, exactly how the mark-price gap windows should be handled.

**Phase 3r recommends Option B (known-invalid-window exclusion for Q6 only)** as primary. The mark-price 5m datasets remain NOT generally research-eligible under the original Phase 3p §4.7 strict gate. *If* Q6 is ever separately authorized as part of a future diagnostics-execution phase, the Q6 analysis must follow a formal exclusion rule (§8) that drops every trade whose Q6 analysis window intersects a known invalid window, reports the excluded counts explicitly, labels Q6 conclusions as conditional on valid mark-price coverage, and is barred from authorizing any prior-verdict revision, strategy rescue, parameter change, or live-readiness implication.

**Phase 3r does not authorize Q6.** Phase 3r does not authorize any diagnostics-execution. Phase 3r is a governance memo only.

## 2. Authority and boundary

Phase 3r operates strictly inside the post-Phase-3q boundary:

- **Predeclaration discipline.** Phase 3o §5 (Q1–Q7 question set), §6 (forbidden question forms), §7 (diagnostic-term definitions), §10 (allowed-vs-forbidden analysis boundary) all preserved verbatim.
- **Outcome-interpretation rules.** Phase 3p §8 (per-Q informative / non-informative / ambiguous thresholds, predeclared *before* any 5m data exists) preserved verbatim.
- **Strict integrity gate.** Phase 3p §4.7 (gaps_detected = 0; monotone_timestamps = true; boundary_alignment_violations = 0; close_time_consistency_violations = 0; OHLC sanity = 0; volume sanity = 0 where applicable; symbol/interval consistency = 0; date_range_coverage = true) preserved verbatim. Phase 3r does NOT relax §4.7.
- **Project-level locks.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) preserved verbatim.
- **Phase 2f thresholds.** §10.3 (Δexp ≥ +0.10 R), §10.4 (absolute floors), §11.3 (V-window no-peeking), §11.4 (ETH non-catastrophic), §11.6 (8 bps HIGH per side cost-resilience) preserved verbatim.
- **Retained-evidence verdicts.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. All preserved verbatim.

Phase 3r adds *governance language* (a formal exclusion rule for Q6 if it is ever run) without adjusting Phase 3p §4.7 itself. The strict gate at §4.7 still classifies the mark-price 5m datasets as not research-eligible. The Phase 3r exclusion rule is a *future-Q6-only* secondary policy that operates within Phase 3p §10's analysis-boundary constraints.

## 3. Starting state

```text
branch:           phase-3r/mark-price-gap-governance
parent commit:    3078b448e5850f943079899c9048b2c19e07adb3 (Phase 3q closeout)
working tree:     clean
main:             9428b05044d57dbd3a1a5739a2b8b1db418dcade (unchanged from post-Phase-3p)
Phase 3q branch:  pushed to origin at 3078b44 (not merged)
```

The Phase 3q acquisition commit `8d99375` and Phase 3q closeout commit `3078b44` are both on the Phase 3q branch, pushed but not merged. The Phase 3q local filesystem evidence (4 manifests, 204 ZIPs, 204 Parquet files, ≈ 147 MB) is `data/**`-gitignored per repo convention identical to v002.

No code under `src/prometheus/` modified by Phase 3r. No script under `scripts/` modified by Phase 3r. No `data/` artefact modified by Phase 3r.

## 4. Phase 3q evidence recap

For governance-memo readability, the relevant Phase 3q findings are recapped here (the authoritative source remains `2026-04-30_phase-3q_5m-data-acquisition-and-integrity-validation.md`):

### 4.1 Trade-price 5m datasets — research-eligible

| Dataset | Bars | Gaps | Other checks | `research_eligible` |
|---|---|---|---|---|
| `binance_usdm_btcusdt_5m__v001` | 446 688 | 0 | all PASS | **true** |
| `binance_usdm_ethusdt_5m__v001` | 446 688 | 0 | all PASS | **true** |

Acquired range `[1640995200000, 1775001300000]` ms is a strict superset of the retained-evidence trade range `[1641014100000, 1770879600000]` ms.

### 4.2 Mark-price 5m datasets — NOT research-eligible

| Dataset | Bars | Gaps | Other checks | `research_eligible` |
|---|---|---|---|---|
| `binance_usdm_btcusdt_markprice_5m__v001` | 445 819 | **4** | all PASS | **false** |
| `binance_usdm_ethusdt_markprice_5m__v001` | 446 106 | **4** | all PASS | **false** |

### 4.3 Mark-price gap windows (recorded in manifests `invalid_windows` and `quality_checks.gap_locations`)

**BTCUSDT mark-price 5m:**

```text
1445 min  2022-07-30T23:55:00 UTC  ->  2022-08-01T00:00:00 UTC
1445 min  2022-10-01T23:55:00 UTC  ->  2022-10-03T00:00:00 UTC
1445 min  2023-02-23T23:55:00 UTC  ->  2023-02-25T00:00:00 UTC
  30 min  2023-11-10T03:35:00 UTC  ->  2023-11-10T04:05:00 UTC
```

**ETHUSDT mark-price 5m:**

```text
  10 min  2022-07-12T13:10:00 UTC  ->  2022-07-12T13:20:00 UTC
1445 min  2022-10-01T23:55:00 UTC  ->  2022-10-03T00:00:00 UTC
1445 min  2023-02-23T23:55:00 UTC  ->  2023-02-25T00:00:00 UTC
  30 min  2023-11-10T03:35:00 UTC  ->  2023-11-10T04:05:00 UTC
```

The total gap volume per symbol is small relative to the 51-month population: BTC 869 missing bars (≈ 0.19% of 446 688 expected); ETH 582 missing bars (≈ 0.13%). The dominant gaps are the three ~24-hour Binance maintenance windows on 2022-10-02, 2023-02-24, plus a third (2022-07-30/31 for BTC, 2022-07-12 for ETH).

### 4.4 v002 precedent

The same 4-window gap pattern was verified to be present in the locked v002 mark-price 15m datasets (`binance_usdm_btcusdt_markprice_15m__v002`, `binance_usdm_ethusdt_markprice_15m__v002`). The v002 manifest's `invalid_windows: []` field was technically inaccurate but the v002 datasets have been used in all retained-evidence backtests (Phase 2e through Phase 3j) without operator-flagged issue. **This v002 precedent does NOT by itself authorize Phase 3q to mark its mark-price 5m datasets research-eligible** — Phase 3q chose strict §4.7 enforcement, which Phase 3r preserves.

### 4.5 No relaxation, no patch, no inference

Phase 3q applied no forward-fill, no interpolation, no imputation, no patch, and no §4.7 relaxation. Mark-price 5m datasets are explicitly recorded `research_eligible: false` and the gap windows are recorded verbatim. Phase 3r continues that posture.

## 5. Governance problem

The governance question Phase 3r must answer is exactly:

> **What is the formally approved governance handling for known mark-price maintenance-window gaps before any possible 5m diagnostics-execution phase is authorized?**

Five sub-questions sit underneath that umbrella:

1. **Eligibility.** Should the mark-price 5m datasets ever be treated as "research-eligible" given known gaps?
2. **Q6 disposition.** Should Phase 3o / 3p Q6 (mark-vs-trade stop-trigger sensitivity) be permanently dropped, or conditionally allowed under specific exclusion rules?
3. **Patch policy.** Are forward-fill / interpolation / imputation / replacement ever permissible for known gaps in this project?
4. **Phase 3p §4.7 amendment.** Should Phase 3p §4.7 itself be amended to allow `research_eligible: true` for datasets with documented invalid windows?
5. **v002 precedent reckoning.** Does the existence of the same gap pattern in v002 imply anything about retained-evidence verdict reliability?

Phase 3r answers each below.

## 6. Options considered

### 6.1 Option A — Keep strict Phase 3p §4.7 unchanged; rule out all mark-price-dependent diagnostics

**Description:** Phase 3p §4.7 stays exactly as-written. Mark-price 5m datasets remain `research_eligible: false`. Q6 (mark-vs-trade stop-trigger sensitivity) is **dropped permanently** under current locked spec. Trade-price diagnostics (Q1, Q2 trade-price-side, Q3, Q5) could still proceed if a future diagnostics-execution phase is separately authorized — but Q6 is structurally blocked.

**Pros:**
- Simplest governance posture. No new rule, no exclusion logic, no edge-case carve-outs.
- Highest predeclaration purity: §4.7 stands as Phase 3p wrote it.
- Eliminates the temptation to rescue Q6 via creative gap-handling.

**Cons:**
- Permanently drops Q6 even though the 4 gap windows total < 0.2% of the 51-month range.
- Q6 was the *specific* mechanism question for understanding mark-price-vs-trade-price stop-trigger divergence — relevant to all candidates but especially R3, F1, D1-A STOP-exit populations. Permanently dropping it forecloses one diagnostic axis.
- The forecast loss is bounded (Q6 was MEDIUM-relevance for most candidates per Phase 3o §11), so this is not a catastrophic loss.

### 6.2 Option B — Treat known mark-price gaps as documented invalid windows; allow Q6 only with explicit exclusion

**Description:** Mark-price 5m datasets remain NOT generally research-eligible under the original Phase 3p §4.7 strict gate (no manifest re-issue, no `research_eligible` flag flip). *If* Q6 is ever authorized in a future diagnostics-execution phase, Q6 may proceed under a formal exclusion rule:

- Every trade whose Q6 analysis window intersects a known invalid window must be excluded from Q6.
- Excluded counts must be reported by candidate, symbol, side, exit type, and gap window.
- Q6 output must be labeled "conditional on valid mark-price coverage."
- No forward-fill, interpolation, imputation, or patching is allowed.
- No diagnostic may infer behavior inside invalid windows.
- No Q6 result may be used to revise prior verdicts automatically.

**Pros:**
- Preserves §4.7 strict gate verbatim (no precedent of post-hoc loosening).
- Allows Q6 to operate on the ~99.8% of bars that are present, with a transparent exclusion-count footnote.
- The exclusion is bounded, predeclared, and auditable (the gap windows are fixed and recorded in the manifests).
- Aligns with the retained-evidence convention of "report what you can, exclude what you can't, document everything." Patch-vs-exclude is the canonical safe choice.
- v002 precedent does NOT leak: the v002 verdicts were produced under v002's flawed but accepted manifest; Phase 3r's Q6 exclusion rule is forward-looking only.

**Cons:**
- Adds a small amount of governance machinery (the exclusion rule + the exclusion-count reporting requirement).
- Requires the future diagnostics-execution phase to implement the exclusion correctly. Misimplementation would produce misleading Q6 results.
- Q6 power is reduced because excluded trades are dropped, not analyzed.

**Phase 3r's view:** This is the recommended option. Reasoning is summarized in §7 below.

### 6.3 Option C — Amend Phase 3p §4.7 to permit documented invalid windows as research-eligible

**Description:** Phase 3p §4.7 is amended (in a separate, explicit, limited amendment memo) to add: "datasets with fully-disclosed `invalid_windows` covering ≤ X% of the date range *may be* `research_eligible: true` if the consuming analysis explicitly handles invalid windows in a documented manner." Mark-price 5m datasets would then have their manifests re-issued with `research_eligible: true` (under the amended rule).

**Pros:**
- Closest to "what v002 implicitly did" — codifies the v002 precedent into formal policy.
- Mark-price 5m datasets become broadly available for any future analysis (not just Q6).
- Removes the procedural awkwardness of having `research_eligible: false` data in active use.

**Cons:**
- Weakens the predeclared strict gate. Phase 2y §11.3.5 explicitly forbids post-hoc loosening; while §4.7 itself is not a strategy threshold, amending it after Phase 3q has run is in tension with the "predeclare, then live with the result" discipline that Phase 3o / 3p / 3q established.
- Requires manifest re-issue for both Phase 3q mark-price datasets, which is non-trivial governance work that breaks the "v001 was published, accept it as-is" cleanliness.
- Risks creating a precedent where future "documented invalid windows" become the default escape hatch from §4.7. Slippery-slope risk.
- Does not provide additional analytical power that Option B doesn't already provide — both still need exclusion logic at the analysis layer to handle gap-window trades.

**Phase 3r's view:** Not recommended. The marginal benefit over Option B is small; the precedent risk is real.

### 6.4 Option D — Seek alternative mark-price source before any Q6 work

**Description:** Defer Q6 governance until an alternative mark-price source is found (or rule it out if no such source exists). Phase 3r would not produce a final Q6 disposition in this option; instead it would commission a separate sourcing memo.

**Pros (in principle):**
- Could in principle close the gaps if an alternative source has the missing bars.

**Cons:**
- The four gap windows correspond to actual Binance exchange-maintenance periods. Mark-price was likely not published at all (not just unavailable in the bulk archive) during those windows. `GET /fapi/v1/markPriceKlines` REST is unlikely to fill the gaps because the upstream data doesn't exist. Third-party derived mark-price reconstructions are unreliable and would introduce a source-of-truth split for v1.
- Phase 3r's brief explicitly forbids data acquisition, REST calls, external sources, and any download. So Option D would either (a) produce a "punt" memo that defers without resolving, or (b) require yet another phase.
- The realistic outcome of Option D is either rediscovering Option A (drop Q6) or Option B (exclude gaps) after additional investigation that Phase 3r already does in §7 below.

**Phase 3r's view:** Not practically distinguishable from Option A/B; not recommended as primary.

### 6.5 Option E — Drop Q6 permanently; proceed only with trade-price diagnostics if later authorized

**Description:** Phase 3o Q6 is formally retired. Future diagnostics-execution may authorize Q1 / Q2 (trade-price-side) / Q3 / Q5 / Q7 only.

**Pros:**
- Clean permanent decision.
- Forecloses the slippery slope of "let's just exclude these gaps and run Q6 anyway."

**Cons:**
- Functionally equivalent to Option A. Distinguishable only by whether Q6 is "blocked under current spec" (Option A) or "permanently retired" (Option E).
- The information-loss claim is bounded: Q6's mechanism contribution to candidate diagnostics was MEDIUM at best per Phase 3o §11. Permanently retiring it forecloses ~20% of the diagnostic surface for STOP-exit population analysis.
- Option B preserves Q6 as a *possible future option* under exclusion; Option E removes it from the menu entirely.

**Phase 3r's view:** Option E is too restrictive. Option B retains optionality without committing to execution.

## 7. Recommended governance decision

**Phase 3r recommends Option B (known-invalid-window exclusion for Q6 only).**

### 7.1 Reasoning summary

1. **§4.7 stays unchanged.** The Phase 3p strict integrity gate remains exactly as-written. Mark-price 5m datasets remain `research_eligible: false`. No manifest re-issue. No precedent of post-hoc loosening.
2. **No patching.** Forward-fill, interpolation, imputation, replacement, and any other form of "filling in" missing bars is **categorically prohibited**. The four gap windows are exclusion zones, not patch zones.
3. **Q6 remains optional but bounded.** *If* a future diagnostics-execution phase is ever authorized AND the operator authorizes Q6 specifically, Q6 may run under a formal exclusion rule (§8 below). *If* Q6 is not authorized, the rule simply never fires.
4. **Trade-price datasets unaffected.** Q1 / Q2 (trade-price-side) / Q3 / Q5 / Q7 do not depend on mark-price data and are not affected by the gap windows. These remain governed by the Phase 3o / 3p discipline as already written.
5. **No prior-verdict revision.** v002 verdicts were produced with the same gap pattern present in v002 mark-price 15m. Phase 3r does not re-open those verdicts. The retained-evidence trade populations for R3 / R2 / F1 / D1-A remain dataset-version-attributed to v002 and are not revised by Phase 3r.
6. **Bounded information loss.** Q6 power is reduced by the exclusion (some trades dropped) but not eliminated. The total gap volume (< 0.2% of bars) makes the exclusion rate small in expectation.
7. **Audit-ready.** The exclusion rule + exclusion-count reporting requirement makes Q6 outputs fully auditable: any reader can verify exactly how many trades were excluded, by which gap window, by which candidate / symbol / side / exit-type combination.

### 7.2 What Option B does NOT do

- Does NOT authorize Q6 execution. Phase 3r is governance-only.
- Does NOT authorize any diagnostics-execution phase. Phase 3o / 3p / 3q predeclaration remains predeclaration; nothing has been run.
- Does NOT amend Phase 3p §4.7. The strict gate stays at-spec.
- Does NOT relax §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3.
- Does NOT revise R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A verdicts.
- Does NOT modify v002 datasets, v002 manifests, or v002-precedent records.
- Does NOT modify the Phase 3q manifests (they remain at `research_eligible: false`).
- Does NOT authorize any 5m strategy, hybrid, variant, rescue, parameter change, or live-readiness implication.

## 8. Formal rule for invalid-window handling (Q6 exclusion rule)

The following formal rule is the mandatory governance specification any future diagnostics-execution phase must obey *if Q6 is ever authorized*. The rule is named **"Q6 invalid-window exclusion rule (Phase 3r §8)"** and is stated here in its full normative form:

### Rule statement

1. **Known invalid windows are exclusion zones, not patch zones.** The four mark-price 5m gap windows recorded in `binance_usdm_btcusdt_markprice_5m__v001.manifest.json` and `binance_usdm_ethusdt_markprice_5m__v001.manifest.json` (`invalid_windows` field) are the canonical invalid windows for this rule. No additional invalid windows may be silently introduced; if new windows are discovered they must be added in a separately authorized governance memo amending §8.
2. **No forward-fill, no interpolation, no imputation, no replacement, no synthetic mark-price data.** No analysis may use any value derived from any source other than the published `data.binance.vision` mark-price 5m bars. No statistical imputation. No interpolated bar. No "missing bar treated as last observed." No mark-price reconstructed from trade-price.
3. **Per-trade exclusion test.** For each trade in the Q6 input population (the v002-locked retained-evidence STOP-exited trade populations), the diagnostics-execution phase must determine the *Q6 analysis window* for that trade — i.e., the time interval during which mark-price observation is required to compute the Q6 statistic for that trade. If the trade's Q6 analysis window intersects any invalid window (for the relevant symbol's mark-price dataset), the trade must be **excluded from Q6**.
4. **Excluded trades must be counted and reported.** The Q6 output must include an exclusion-counts table with at minimum the following columns:
   - Candidate (R3, R2, F1, D1-A).
   - Symbol (BTCUSDT, ETHUSDT).
   - Side (long, short).
   - Exit type (STOP, TARGET, TIME_STOP, etc.).
   - Gap window identifier (one of the eight recorded gap windows across BTC + ETH).
   - Excluded trade count.
5. **Q6 conclusions must be labeled conditional on valid mark-price coverage.** Any narrative summary of Q6 output must include the phrase "conditional on valid mark-price coverage" or equivalent. The labeling cannot be omitted, abbreviated, or buried. A Q6 finding without the conditional label is not a valid Q6 output.
6. **No automatic prior-verdict revision.** No Q6 finding — informative, non-informative, ambiguous — may by itself revise R3 baseline-of-record, R2 FAILED, F1 HARD REJECT, D1-A MECHANISM PASS / FRAMEWORK FAIL — other, or any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold. Verdict revision requires a separately authorized formal reclassification phase with predeclared evidence thresholds.
7. **No strategy rescue, no parameter change, no live-readiness implication.** Q6 outputs are descriptive evidence only. They cannot license:
   - Stop widening (forbidden by `.claude/rules/prometheus-safety.md` regardless of Q6).
   - Stop policy revision.
   - §1.7.3 mark-price-stop lock revision.
   - Any retained-evidence candidate revision.
   - Any 5m strategy / hybrid / variant authorization.
   - Any paper/shadow / Phase 4 / live-readiness / deployment authorization.
8. **No silent rule revision.** This Q6 exclusion rule is itself predeclared and immutable from the Phase 3r commit forward. Any future change requires a separately authorized governance memo amending §8 explicitly.
9. **Exclusion test must be documented in the diagnostics-execution plan.** Before any Q6 computation begins, the diagnostics-execution phase brief must specify the exact algorithm for determining each trade's Q6 analysis window. The brief must be predeclared on `main` before the analysis runs.

### Plain-English restatement of the rule

> *If Q6 is ever run, drop any trade whose Q6 needs mark-price during a known gap. Count the dropped trades. Label all Q6 results as conditional on coverage. Never patch the gaps. Never use Q6 to revise verdicts, change parameters, rescue candidates, or imply anything about live-readiness.*

## 9. Q6 disposition

**Phase 3r disposition for Q6:**

- Q6 is **NOT permanently retired**. (Option E rejected.)
- Q6 is **NOT currently authorized**. Phase 3r authorizes nothing.
- Q6 **MAY be authorized** in a future separately-authorized diagnostics-execution phase, subject to the §8 invalid-window exclusion rule.
- *If* authorized, Q6 must operate strictly under §8.
- *If* §8 cannot be implemented in the diagnostics-execution phase (e.g., the per-trade exclusion test fails to be defined precisely), Q6 must be aborted and a failure report written instead of producing partial output.

The Q6 disposition is therefore: **bounded-conditional optionality.** Q6 stays on the menu but only as a §8-bounded option.

## 10. Effect on Q1, Q2, Q3, Q5, and Q7

### 10.1 Q1 (immediate adverse excursion in first 5–15 minutes after entry)

**Effect:** None. Q1 uses trade-price 5m data only. Trade-price 5m datasets are research-eligible. Q1 is unaffected by §8.

### 10.2 Q2 (stop-trigger path: short-lived 5m wick vs sustained invalidation)

**Effect:** Mostly none. Phase 3o §5.2 specified Q2 as a *trade-price-path* classification (wick vs sustained invalidation in the position-relative direction). The trade-price-side of Q2 is unaffected. *If* the diagnostics-execution phase brief later proposes a mark-price-augmented Q2 sub-analysis, that sub-analysis would inherit the §8 rule by extension. The base Q2 (trade-price-only) is unaffected.

### 10.3 Q3 (intrabar +1R / +2R target touches before adverse exit)

**Effect:** None. Q3 uses trade-price 5m data only (high / low extremes for target-touch detection). Trade-price 5m datasets are research-eligible. Q3 is unaffected by §8.

### 10.4 Q5 (next-15m-open fill assumption realism via 5m sub-bar decomposition)

**Effect:** None. Q5 uses trade-price 5m data only. Q5 is unaffected by §8.

### 10.5 Q7 (meta-classification)

**Effect:** Bounded. Q7's classification rule (Phase 3p §8.7) requires ≥ 3 of Q1–Q6 to classify `informative` for Q7 itself to be `informative`. With Q6 conditionally available (under §8), Q7's input set is preserved in expectation; if Q6 is dropped at execution time (e.g., the operator does not authorize Q6, or §8 cannot be implemented), Q7 evaluates over Q1–Q5 only and the threshold remains "≥ 3 of those 5 informative." This minor adjustment is a natural consequence of Q6 being a conditional question. No silent adjustment is required.

### 10.6 Q4 (D1-A funding-extreme decay over 5/10/15/30/60 min)

**Effect:** None. Q4 uses trade-price 5m data + the existing v002 funding-event tables. Q4 is unaffected by §8.

### 10.7 Cross-Q summary

The §8 rule scope is **strictly confined to Q6**. Q1, Q2 (trade-price base), Q3, Q4, Q5, Q7 are unaffected by Phase 3r's governance decision. The trade-price 5m datasets remain research-eligible for any future diagnostics-execution phase that operates on them.

## 11. What remains forbidden

Phase 3r preserves all prior forbidden-work boundaries, with explicit emphasis on:

- **No §4.7 amendment.** The Phase 3p strict integrity gate is unchanged. The mark-price 5m manifests retain `research_eligible: false`.
- **No data patching.** Forward-fill, interpolation, imputation, replacement, synthetic mark-price, and reconstruction-from-trade-price are all categorically forbidden for any analysis subject to §8.
- **No Q6 execution.** Phase 3r does not authorize Q6 computation. Q6 is conditionally permitted *if* later authorized; nothing about Phase 3r constitutes that authorization.
- **No diagnostics-execution authorization.** Phase 3r authorizes nothing. No Q1–Q7 question is run.
- **No prior-verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A verdicts unchanged.
- **No threshold revision.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged.
- **No strategy-parameter revision.** R3 / F1 / D1-A specs unchanged. No hybrid. No variant. No rescue.
- **No project-lock revision.** §1.7.3 unchanged. Mark-price stops remain locked.
- **No paper/shadow / Phase 4 / live-readiness / deployment authorization.**
- **No production-key / exchange-write / credentials / authenticated-API / private-endpoint / user-stream / WebSocket activity.**
- **No MCP / Graphify / `.mcp.json` activation.**
- **No data acquisition / data download / external-source query.** Phase 3r does not call Binance REST, does not download data, does not consult third-party sources.
- **No data modification.** No `data/` artefact modified. No Phase 3q manifest modified. No v002 dataset / manifest modified.
- **No Phase 3p text modification.** Phase 3r is a new governance memo; Phase 3p §4.7 stands as-written.
- **No 5m strategy / hybrid / variant.**
- **No merge to main.**
- **No successor phase started.**

## 12. Prior-verdict and lock preservation

| Item | State |
|------|-------|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1; locked sub-parameters preserved verbatim. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3; preserved verbatim. |
| **R1a / R1b-narrow** | Retained research evidence only; non-leading; preserved verbatim. |
| **R2** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks**; preserved verbatim. |
| **F1** | Retained research evidence only; **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1; preserved verbatim. |
| **D1-A** | Retained research evidence only; **MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec; preserved verbatim. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **Phase 3p §4.7 strict integrity gate** | Preserved verbatim. NOT amended. |
| **v002 dataset families and manifests** | Preserved verbatim. NOT modified. |
| **Phase 3q v001-of-5m manifests** | Preserved verbatim. NOT modified. Mark-price still `research_eligible: false`. |
| **Phase 3o question set Q1–Q7 + forbidden forms + diagnostic terms + analysis boundary** | Preserved verbatim. |
| **Phase 3p data-requirements + dataset-versioning approach + manifest specification + per-question outputs + outcome-interpretation rules** | Preserved verbatim. |
| **Paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write authorization** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

Phase 3r adds a **new** governance rule (§8: Q6 invalid-window exclusion rule) without modifying any existing rule, threshold, dataset, manifest, verdict, lock, or prior phase memo. The new rule is forward-looking only and is binding on any future phase that runs Q6.

## 13. Operator decision menu

The operator now has Phase 3r's governance memo. The next operator decision is operator-driven only.

### 13.1 Option A — Adopt Phase 3r §8 as the binding Q6 exclusion rule; remain paused (PRIMARY recommendation)

**Description:** The operator approves Phase 3r §8 as the formally binding governance rule for any future Q6 execution. Phase 3r is merged when convenient. No diagnostics-execution phase is authorized. Strategy execution remains paused.

**Effect:** Phase 3r §8 becomes immutable from the operator-approval point forward. Future diagnostics-execution phases are bound to it. No Q6 has run. No Q1–Q5 / Q7 has run. No 5m strategy. No verdict revision.

**Why primary:** The 5m research thread now has a complete, predeclared, immutable specification spanning Phase 3o (questions + forbidden forms + terms + boundary), Phase 3p (data requirements + versioning + manifest spec + per-question outputs + outcome-interpretation rules), Phase 3q (acquisition + integrity validation), and Phase 3r (mark-price gap governance + Q6 exclusion rule). Whether to *act on* the specification is a separate operator-strategic decision the operator can make later or never. Phase 3r's value is realized by the predeclaration itself; running anything is not necessary for that value.

### 13.2 Option B — Adopt Phase 3r §8 AND authorize a future docs-only diagnostics-execution phase (CONDITIONAL secondary alternative)

**Description:** The operator approves Phase 3r §8 AND authorizes a future docs-only phase that runs Q1, Q2 (trade-price), Q3, Q5, Q7, and (optionally) Q6 under §8. Phase 3r is merged. The diagnostics-execution phase is separately briefed and started.

**Pre-conditions if selected:**
- Operator commits ex-ante to anti-circular-reasoning discipline (Phase 3o §6, Phase 3p §10).
- Operator commits that the diagnostics-execution phase cannot revise prior verdicts, change parameters, rescue candidates, or imply live-readiness.
- Operator commits that any §8 implementation choice is predeclared in the diagnostics-execution phase brief before computation begins.
- Operator explicitly decides Q6 disposition: (a) include Q6 under §8, or (b) skip Q6 entirely.

**Risks if selected:**
- Procedural escalation. Six docs-only / docs-and-data phases on the 5m thread (3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r) have now produced complete predeclaration + acquisition + governance. Adding a runtime phase is a discrete escalation that should be done only with clear strategic motivation.
- A `non-informative` Q7 outcome (statistically the most likely, per Phase 3p §8.7 reasoning) would functionally close the 5m thread without action — the operator should be prepared to face that outcome honestly.

### 13.3 Option C — Adopt §8, run Q6 only, skip the rest (NOT RECOMMENDED)

Running Q6 alone (without Q1 / Q2 / Q3 / Q5 / Q7) gives narrow mechanism evidence with no broader context for interpretation. Q7's meta-classification cannot fire on Q6 alone. Not a coherent operational choice.

### 13.4 Option D — Adopt §8 AND amend Phase 3p §4.7 in the same step (NOT RECOMMENDED)

Combining a governance amendment with a rule adoption is procedurally messier than keeping them separate. If §4.7 amendment is ever desired, it should be a separately authorized memo. Phase 3r preserves §4.7.

### 13.5 Option E — Reject Phase 3r entirely; permanently retire Q6 (Option E from §6)

**Description:** Operator declines §8 and permanently retires Q6. Mark-price 5m datasets remain `research_eligible: false` permanently. Future diagnostics may run only Q1 / Q2 / Q3 / Q5 / Q7.

**Phase 3r's view:** Acceptable but more restrictive than necessary. Functionally similar to Option A above but forecloses the Q6 option. Not recommended as primary.

### 13.6 Option F — Strategy rescue / new strategy / regime-first / ML / paper-shadow / Phase 4 / live-readiness / deployment (NOT RECOMMENDED)

Phase 3r changes nothing about the post-Phase-3p / 3q strategic boundary. None of these are appropriate. Strongly not recommended.

### 13.7 Recommendation

**Phase 3r recommends Option A (adopt §8; remain paused) as primary.** Phase 3r §8 becomes the binding governance rule for any future Q6 execution. No diagnostics phase is authorized. No verdict revised. No project-lock revised. No threshold revised. R3 baseline-of-record and all retained-evidence verdicts preserved. Recommended state remains **paused**.

Phase 3r explicitly does NOT recommend:

- Q6 execution.
- Any diagnostics-execution.
- Phase 3p §4.7 amendment.
- Manifest re-issue for the Phase 3q mark-price datasets.
- Prior-verdict revision.
- Strategy rescue.
- 5m strategy / hybrid / variant.
- Paper/shadow / Phase 4 / live-readiness / deployment.
- Production-key / exchange-write / credentials / MCP / Graphify / `.mcp.json` activation.

## 14. Next authorization status

**No next phase has been authorized.** Phase 3r authorizes nothing other than the in-memo §8 governance rule itself, which is forward-binding on any future Q6-running phase but does not start such a phase. The operator's next decision is: whether to (a) merge Phase 3r and keep paused, (b) merge Phase 3r and authorize a separately briefed diagnostics-execution phase, (c) reject Phase 3r and permanently retire Q6, or (d) reject Phase 3r and request changes. No such decision has been made.
