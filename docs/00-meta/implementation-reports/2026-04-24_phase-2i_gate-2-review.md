# Phase 2i — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2i/structural-redesign-planning` (created from `main` at `61696a6` — verified clean working tree, synchronized with `origin/main` after the Phase 2h PR #9 merge)
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2i), awaiting operator / ChatGPT Gate 2 approval
**Scope:** Pre-commit review of the Phase 2i docs-only deliverables against the Phase 2i Gate 1 plan and the operator's three Gate 1 conditions. No `git add` / `git commit` has been run. Quality gates green; pytest 396 passing.

---

## Phase

**Phase 2i — Structural Breakout Redesign Planning.**

Decision/planning-only phase following the Phase 2h provisional recommendation (Option B Structural Breakout Redesign Planning). Goal: define structural-vs-parametric for the v1 family explicitly enough to prevent quietly relabeling parameter tweaks; evaluate five redesign axes; propose a candidate shortlist with each candidate as a genuine rule-shape change; surface GAP-030/031/032/033 interactions per candidate; reuse Phase 2f §10.3/§10.4/§11.3/§11.4/§11.6 thresholds and the GAP-036 fold scheme without modification; recommend a carry-forward set capped at ≤ 2 per the operator's Gate 1 condition 1; explicitly test R1's coherence per condition 2; record an explicit H0-anchor statement per condition 3.

## 1. Scope confirmed against Gate 1 plan

Match against `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` §§ 4–14.A and §§ 25–26 execution sequence and conditions.

| Gate 1 requirement                                                                                | Status  | Location of evidence                                                                                          |
|---------------------------------------------------------------------------------------------------|---------|---------------------------------------------------------------------------------------------------------------|
| Factual recap of Phase 2e/2f/2g/2h                                                                | Done    | Memo Part 1 §§ 1.1–1.6 (with citations to source committed reports)                                            |
| Definition of structural redesign — binding test                                                  | Done    | Memo Part 1 §1.7 (4 sub-items: structural / parametric / fixed locks / not-silently-redefined)                |
| Redesign-axis analysis (5 families)                                                               | Done    | Memo Part 2 §§ 2.1.1–2.1.5 (rationale / evidence / expected effects / overfitting / complexity / validation)  |
| Redesign-candidate shortlist (rule-shape changes only)                                            | Done    | Memo Part 2 §2.3 (4 candidates: R1a, R1b, R2, R3 — each with thesis / problem / replaced-vs-kept / new risks)  |
| **Gate 1 condition 1: ≤ 2 carry-forward to Phase 2j**                                             | Done    | Memo Part 3 §3.2 explicit cap recorded; carry-forward set is exactly 2 (R1a + R3); R1b and R2 explicitly excluded |
| **Gate 1 condition 2: R1 coherence requirement**                                                  | Done    | Memo Part 2 §2.2 with three sub-items (unifying-thesis case, separable-ideas case, conclusion). Conclusion: R1 IS two separable ideas; split into R1a and R1b. No bundled candidate is carried forward. |
| **Gate 1 condition 3: H0 anchor wording**                                                         | Done    | Memo Part 2 §2.5.1 with two binding statements (H0 only anchor; wave-1 variants historical-only). §3.5 reaffirms in non-proposal list. |
| GAP-030/031/032/033 disposition matrix per candidate                                              | Done    | Memo Part 2 §2.4 (4-candidate × 4-GAP matrix with explicit CARRIED / SUPERSEDED / CARRIED-AND-EXTENDED labels) |
| Validation framework with thresholds + fold scheme + mandatory diagnostics                        | Done    | Memo Part 2 §§ 2.5.1–2.5.6                                                                                    |
| Relationship to fallback Wave 2                                                                   | Done    | Memo Part 2 §2.6                                                                                              |
| Relationship to Phase 4                                                                           | Done    | Memo Part 2 §2.7                                                                                              |
| Recommendation (provisional primary + fallback)                                                   | Done    | Memo Part 3 §§ 3.1, 3.3                                                                                       |
| "What would change this recommendation"                                                           | Done    | Memo Part 3 §3.4 with five switch-condition blocks                                                            |
| Explicit non-proposal list                                                                        | Done    | Memo Part 3 §3.5                                                                                              |
| Wave-1 result preserved (REJECT ALL); no re-derivation                                            | Done    | Memo Part 1 §1.3 quotes Phase 2g verbatim; Part 3 §3.5 explicit non-proposal list                              |
| Phase 2h provisional recommendation preserved (not re-framed)                                     | Done    | Memo Part 1 §1.4 records Phase 2h as input; Part 3 §3.1 carries the provisional / evidence-based framing       |
| Threshold preservation (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged)                          | Done    | Memo §2.5.2 reuses Phase 2f thresholds; §3.5 explicit non-proposal list                                        |
| §1.7.3 project-level locks preserved                                                              | Done    | Memo §1.7.3 enumerates locks; §2.1.5 explicitly excludes Family-R candidates that violate one-position lock    |
| Gate 1 plan committed to docs                                                                     | Done    | `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` (untracked draft updated with §26 conditions; will be committed in commit 1) |
| Gate 2 review committed to docs                                                                   | Done    | this file                                                                                                     |

**No scope diffs from the approved Gate 1 plan.** All three operator Gate 1 conditions are honored.

## 2. Docs written in Phase 2i

- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` — Gate 1 plan with all three operator conditions applied inline (§26).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md` — three-part redesign-analysis memo (Part 1 Factual recap + structural-vs-parametric definition; Part 2 5-axis evaluation + R1 coherence test + 4-candidate shortlist + GAP matrix + validation framework + fallback/Phase-4 relationships; Part 3 ≤ 2 carry-forward recommendation + provisional primary/fallback + switch conditions + non-proposal list).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md` — this review.

**No ambiguity-log appends.** The §1.7 binding test, the Phase 2f §9.1 / §10.3 / §10.4 / §11.3 thresholds, and the Gate 1 condition framework handled every structural-vs-parametric judgement made in this memo. No new ambiguity surfaced that required a permanent ambiguity-log entry. Specifically:

- The R1 coherence test (memo §2.2) was resolved using the §1.7 binding test (rule-shape vs. parametric distinction) — no spec ambiguity, just a memo-level analytical conclusion.
- The Family-R exclusion (memo §2.1.5) was resolved using §1.7.3 project-level locks — no spec ambiguity, just an enforcement of existing locks.
- The R3 fixed-R vs. H-D6 distinction (memo §2.6) was resolved using Phase 2f §9.1 (single-axis vs. parametric variants) — no spec ambiguity.

The Phase 2i Gate 1 plan §19 anticipated this: "At most one new GAP entry, conditional on the analysis surfacing a clean structural-vs-parametric ambiguity in the v1 spec... If no new GAP is needed, the ambiguity log is unchanged."

**No other files touched.** No `src/` edits. No `tests/` edits. No `scripts/` edits. No `pyproject.toml` edits. No `configs/` edits. No `.claude/` edits. No `data/` writes. No `docs/12-roadmap/technical-debt-register.md` edits. No edits to existing ambiguity-log entries.

## 3. Three Gate 1 conditions — verbatim verification

### Condition 1 — ≤ 2 carry-forward to Phase 2j

Memo §3.2 records the carry-forward set explicitly:

- **Recommended carry-forward (provisional): R1a + R3** (exactly 2).
- **NOT recommended for carry-forward: R1b, R2** (with reasoning).

The cap is binding. Operator may choose a different pair within the cap.

### Condition 2 — R1 coherence requirement

Memo §2.2 contains:

- §2.2.1 — the unifying-thesis case (defending R1 as one coherent thesis).
- §2.2.2 — the separable-ideas case (arguing R1 is two ideas).
- §2.2.3 — conclusion: R1 IS two separable ideas. Split into R1a (Family-S setup-pattern volatility-percentile) and R1b (Family-B HTF bias/regime).

The 4-candidate shortlist (§2.3) reflects the split. R1 as a bundled candidate is not carried forward.

### Condition 3 — H0 anchor wording

Memo §2.5.1 contains the two binding statements:

- "H0 remains the only comparison anchor for redesign candidates."
- "Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines."

§3.5 reaffirms in the explicit non-proposal list ("Any comparison of redesigned candidates to wave-1 variants as promotion baselines"). Memo §2.5.6 elaborates on why redesigned candidates compare to H0 and not to each other (avoiding implicit-tournament peeking).

## 4. Factual recap completeness

The memo's Part 1 cross-checks against source committed reports:

- §1.1 Phase 2e baseline numbers — quoted from `2026-04-20_phase-2e-baseline-summary.md` (BTC 41/29.27%/−0.43/0.32/−3.95%/−4.23%; ETH 47/23.40%/−0.39/0.42/−4.07%/−4.89%). Funnel rejection percentages match source.
- §1.2 Phase 2f conclusions — quoted from `2026-04-24_phase-2f_strategy-review-memo.md` and Gate 1 plan. §10.3 / §10.4 / §11.3 / §11.4 / §11.6 wording mirrored.
- §1.3 Phase 2g wave-1 result — full headline table quoted from `2026-04-24_phase-2g_wave1_variant-comparison.md` §1; per-fold pattern matches §3.
- §1.4 Phase 2h provisional recommendation — quoted from `2026-04-24_phase-2h_decision-memo.md` §3.1.

No re-derivation. No re-ranking. No threshold reframe.

## 5. Structural-vs-parametric definition

Memo §1.7 contains four binding sub-items:

- §1.7.1 What counts as structural — five categories (rule shape, rule input domain, rule output coupling, trade-lifecycle topology, risk/position-management new dimension).
- §1.7.2 What counts as parametric (NOT structural) — four categories (numeric threshold, window length, indicator period, parametric bundle).
- §1.7.3 What remains fixed — six project-level locks.
- §1.7.4 What must not be silently redefined — six items (§10.3 floor, §11.3 discipline, §11.4 ETH rule, §11.3.5 pre-committed thresholds, wave-1 verdict, Phase 2h provisional recommendation).

The binding test prevents Phase 2j from quietly relabeling parameter tweaks as "structural".

## 6. Five-axis evaluation completeness

Memo §§ 2.1.1–2.1.5 cover all five axes per Gate 1 plan §8:

- §2.1.1 Family S setup-pattern (rationale / evidence / candidate-shapes / 4 effect-and-burden columns).
- §2.1.2 Family B HTF bias/regime (same structure).
- §2.1.3 Family E entry-timing (same structure).
- §2.1.4 Family X exit-philosophy (same structure).
- §2.1.5 Family R risk/position-management (same structure + explicit exclusion rationale via §1.7.3 lock).

## 7. Candidate shortlist

Memo §2.3 lists four candidates after the §2.2 R1 split:

| Candidate | Family | Thesis | Replaced | Kept | New risks |
|---|---|---|---|---|---|
| R1a | S | Volatility-percentile setup | Setup-pattern (range-based ratio → vol-percentile ranking) | 8-bar window, 15m signal, 1h bias, structural stop, all §1.7.3 locks | Implicit sub-parameters (percentile threshold, lookback-N) |
| R1b | B | ADX/regime HTF bias | HTF bias rule (EMA-pair + slope → ADX or regime classifier) | 1h timeframe, setup, trigger, stop, exit, all §1.7.3 locks | ADX threshold parametric; cross-symbol robustness harder |
| R2 | E | Pullback-confirmed entry | Entry-timing (next-bar-open → pending limit valid for N bars) | Setup, bias, trigger, stop, exit, all §1.7.3 locks | Lower trade count; new pending-limit-fill logic needed |
| R3 | X | Fixed-R exit with time stop | Exit philosophy (Stage 3–7 staged-trailing → fixed-2R + 8-bar fallback) | Setup, bias, trigger, entry, structural stop, all §1.7.3 locks | Fixed-2R may clip big winners; R-multiple choice must be pre-committed |

Each is a single-axis structural rule-shape change. Multi-axis bundling forbidden (R1 split per §2.2).

## 8. GAP disposition matrix

Memo §2.4 contains the 4-candidate × 4-GAP matrix:

| GAP | R1a | R1b | R2 | R3 |
|---|---|---|---|---|
| 030 break-even rule-text | CARRIED | CARRIED | CARRIED | SUPERSEDED |
| 031 EMA slope wording | CARRIED | SUPERSEDED | CARRIED | CARRIED |
| 032 mark-price sensitivity (mandatory report cut) | CARRIED | CARRIED | CARRIED | CARRIED |
| 033 stagnation window | CARRIED | CARRIED | CARRIED | CARRIED-AND-EXTENDED |

Each candidate's Phase 2j spec will mark SUPERSEDED GAPs in the ambiguity log when execution begins (not in Phase 2i).

## 9. Validation framework

Memo §§ 2.5.1–2.5.6 cover all required elements:

- §2.5.1 H0 anchor + wave-1-historical-only (Gate 1 condition 3).
- §2.5.2 Pre-declared thresholds (reused from Phase 2f).
- §2.5.3 Per-candidate spec must pre-declare rule shape, sub-parameter values (no sweeps), thresholds, candidate-specific success criteria.
- §2.5.4 R/V split + GAP-036 fold scheme (no change).
- §2.5.5 Mandatory diagnostics (per-regime expR; MFE distribution; long/short asymmetry; mark-price sensitivity per GAP-032).
- §2.5.6 Why candidates compare to H0 not each other (avoiding implicit-tournament peeking).

## 10. Recommendation

Primary (provisional): **Phase 2j Option A — Structural redesign memo only (docs-only)**, with carry-forward set R1a + R3.

Fallback (provisional): **Phase 2j Option B — Redesign candidate execution planning**, applicable only if Phase 2j Option A's spec writing narrows to a single fully-specified candidate.

Phase 4 stays deferred per existing operator policy.

Memo §3.4 records five switch-condition blocks: change carry-forward set; A → B; A → C (fallback Wave 2); A → D (Phase 4); A → defer.

## 11. Wave-1 result preservation

Memo Part 1 §1.3 quotes the wave-1 R-window headline verbatim. §3.5 explicit non-proposal list states "Any re-derivation or re-ranking of the wave-1 result. The verdict is REJECT ALL per Phase 2g and stays REJECT ALL."

## 12. Phase 2h provisional recommendation preservation

Memo §1.4 records Phase 2h's provisional recommendation as input (B primary, A fallback, Phase 4 deferred, four switch-condition blocks). Part 3 §3.1 carries the provisional / evidence-based framing from Phase 2h §3.1 forward into Phase 2i's recommendation. No re-framing.

## 13. Threshold preservation

§10.3 disqualification floor: unchanged.
§10.4 hard reject: unchanged.
§11.3 no-peeking: unchanged.
§11.3.5 pre-declared thresholds, no post-hoc loosening: unchanged.
§11.4 ETH-as-comparison: unchanged.
§11.6 cost-sensitivity: unchanged.

Memo §2.5.2 reuses Phase 2f thresholds explicitly. §3.5 explicit non-proposal list reaffirms.

## 14. §1.7.3 project-level locks preservation

| Lock | Memo location |
|---|---|
| BTCUSDT live primary, ETHUSDT research/comparison | §1.7.3 |
| One-way mode, isolated margin, one position max, one active protective stop max, no pyramiding, no reversal while positioned | §1.7.3 |
| Initial live risk 0.25%, leverage cap 2x, internal notional cap mandatory | §1.7.3 |
| Exchange state authoritative; SAFE_MODE start; mark-price stops | §1.7.3 |
| v002 datasets, manifests, 51-month coverage | §1.7.3 |

Family-R candidates that would violate any lock are excluded per §2.1.5.

## 15. Safety posture

| Check                                            | Result                                                 |
|--------------------------------------------------|--------------------------------------------------------|
| Production Binance keys                          | none                                                   |
| Exchange-write code                              | none                                                   |
| Credentials                                      | none — no `.env`, no secrets in any doc                |
| `.mcp.json`                                      | not created                                            |
| Graphify                                         | not enabled                                            |
| MCP servers                                      | not activated                                          |
| Manual trading controls                          | none                                                   |
| Strategy logic edits                             | none                                                   |
| Risk engine edits                                | none                                                   |
| Data ingestion edits                             | none                                                   |
| Exchange adapter edits                           | none                                                   |
| Binance public URLs                              | none fetched                                           |
| `.claude/settings.json` / `settings.local.json`  | preserved                                              |
| Destructive git commands                         | none run                                               |
| Changes outside working tree                     | none                                                   |
| New dependencies                                 | none — `pyproject.toml` unchanged                      |
| `data/` commits                                  | none staged                                            |
| `technical-debt-register.md` edits               | none (operator restriction)                            |
| Phase 4 work                                     | none (operator restriction)                            |
| Phase 2j work                                    | none (this is the phase that proposes 2j, not starts it) |
| New backtests / variants / data                  | none                                                   |
| Threshold tightening / loosening                 | none                                                   |
| New source, test, script, or config files        | none                                                   |
| Re-derivation of wave-1 verdict                  | none — REJECT ALL preserved                            |
| Re-framing of Phase 2h provisional recommendation | none — Phase 2h is input, not target                   |
| Quietly re-classifying parametric as structural  | none — §1.7 binding test applies; §2.2 R1 coherence test applied |

## 16. Operator restrictions honoured

All three Gate 1 conditions applied (§3 above). All "still forbidden" items from the Gate 1 approval text held: no code changes, no new backtests, no new variants, no data downloads, no API calls, no Phase 4 work, no `technical-debt-register.md` edits, no MCP/Graphify, no `.mcp.json`, no `git add`, no `git commit`, no push.

## 17. Test suite

`uv run pytest` expected to pass **396 tests** (identical to end of Phase 2h). Phase 2i made zero code changes; no test count change is expected. Output captured at the pre-commit stop point.

## 18. Recommended next step

Operator / ChatGPT Gate 2 review of:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md` (this file)

If approved, proceed to the four-commit sequence (Gate 1 plan; redesign-analysis memo; this Gate 2 review; Phase 2i checkpoint report). No ambiguity-log commit since no new GAP is needed (§2 above). After commits, the operator chooses among:

- **Phase 2j Option A (provisional primary)** — Structural redesign memo only (docs-only) with carry-forward set R1a + R3 (or operator-modified pair within the ≤ 2 cap).
- **Phase 2j Option B (provisional fallback)** — Redesign candidate execution planning (Gate 1 plan for executing 1 candidate).
- **Phase 2j Option C** — Fallback narrow Wave 2 with H-D6 (memo §3.4 "switch from A → C").
- **Phase 2j Option D** — Phase 4 (memo §3.4 "switch from A → D"; requires explicit operator policy change).

The recommendation is provisional; the operator's choice is the binding decision.

## 19. Questions for operator / ChatGPT

None. All three Gate 1 conditions have been applied inline. The §3.4 "What would change this recommendation" section makes the switch conditions explicit and pre-declared.

---

**Stop here. No `git add` / `git commit` has run. Awaiting operator / ChatGPT Gate 2 approval.**
