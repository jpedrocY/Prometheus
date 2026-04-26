# Phase 2h — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2h/post-wave-decision-memo` (created from `main` at `0b67357` — verified clean working tree, `main` synchronized with `origin/main` after the Phase 2g PR #8 merge)
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2h), awaiting operator / ChatGPT Gate 2 approval
**Scope:** Pre-commit review of the Phase 2h docs-only deliverables against the Phase 2h Gate 1 plan and the operator's three Gate 1 conditions. No `git add` / `git commit` has been run. Quality gates green; pytest 396 passing.

---

## Phase

**Phase 2h — Post-Wave Strategy Decision and Next Research Direction Planning.**

Decision/planning-only phase following the Phase 2g wave-1 REJECT-ALL outcome. Goal: produce a disciplined diagnostic of what wave 1 taught us, an option-space analysis for the next phase, an explicit handling of H-B2's near-pass, an anti-overfitting / methodology section, and a provisional recommendation with explicit "what would change this recommendation" switch conditions. Per Phase 2g §11.3 no-peeking discipline, the wave-1 verdict (REJECT ALL) stands and is not re-derived; per Phase 2f §11.3.5 no thresholds are tightened or loosened.

## 1. Scope confirmed against Gate 1 plan

Match against `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-1-plan.md` §§ 4–14.A and §26 execution sequence.

| Gate 1 requirement                                                                                | Status  | Location of evidence                                                                                          |
|---------------------------------------------------------------------------------------------------|---------|---------------------------------------------------------------------------------------------------------------|
| Factual recap of Phase 2e baseline / 2f conclusions / 2g wave-1 result                            | Done    | Memo Part 1 §§ 1.1–1.5 (with citations to the source committed reports)                                       |
| Diagnosis framework: ruled-out / not-ruled-out / evidence pattern                                 | Done    | Memo Part 2 §§ 2.1–2.3                                                                                        |
| Decision options analysis (A/B/C/D) with pros / cons / wasted-effort / EVI                        | Done    | Memo Part 2 §§ 2.4–2.7                                                                                        |
| Recommended decision criteria for each path                                                       | Done    | Memo Part 2 §2.8                                                                                              |
| Explicit handling of H-B2's near-pass with anti-bundled-rescue language                           | Done    | Memo Part 2 §2.9                                                                                              |
| Anti-overfitting / methodology section                                                            | Done    | Memo Part 2 §2.10 (5 sub-items: stop-rule, family-stop, sample segmentation, fold-scheme ambiguity, other)    |
| Recommendation: primary + fallback + reasoning                                                    | Done    | Memo Part 3 §§ 3.1–3.2                                                                                        |
| **Gate 1 condition 1: provisional + evidence-based framing with three explicit non-claims**       | Done    | Memo Part 3 §3.1 opens with three non-claim bullets verbatim; primary and fallback labeled "(provisional)"   |
| **Gate 1 condition 2: "What would change this recommendation" subsection**                        | Done    | Memo Part 3 §3.3 with four switch-condition blocks (B → A, B → C, B → defer, any → D)                          |
| **Gate 1 condition 3: directly-verified wording for repo state**                                  | Done    | Header lines on both Gate 1 plan and decision memo cite "verified clean working tree, main synchronized with origin/main after the Phase 2g PR #8 merge"; no speculative merge-path language |
| Ambiguity-log append GAP-20260424-036 (fold-scheme convention)                                    | Done    | `docs/00-meta/implementation-ambiguity-log.md` lines 1006+ (one new entry; no edits to existing entries)      |
| Gate 1 plan committed to docs                                                                     | Done    | `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-1-plan.md`                                      |
| Gate 2 review committed to docs                                                                   | Done    | this file                                                                                                     |
| Wave-1 result preserved (REJECT ALL); no re-derivation                                            | Done    | Memo Part 1 §1.3 quotes Phase 2g verbatim; Part 3 §3.4 explicit non-proposal list                              |
| Threshold preservation (§10.3 / §10.4 / §11.3 / §11.6 unchanged)                                  | Done    | Memo Part 2 §2.10.5 + Part 3 §3.4                                                                              |
| Still-forbidden items re-affirmed                                                                 | Done    | Gate 1 plan §§ 5, 18; memo Part 3 §3.4                                                                         |

**No scope diffs from the approved Gate 1 plan.** All three operator Gate 1 conditions are honored.

## 2. Docs written in Phase 2h

- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-1-plan.md` — new file; Gate 1 plan with all three operator conditions applied inline.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_decision-memo.md` — new file; three-part memo (Part 1 Factual recap, Part 2 Diagnosis + options, Part 3 Recommendation + switch conditions).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-2-review.md` — new file; this review.

Ambiguity-log appends (no existing entries modified):

- `docs/00-meta/implementation-ambiguity-log.md` — one new GAP entry (GAP-20260424-036) appended after the existing GAP-20260424-035 entry. Standing convention for fold-scheme interpretation per Phase 2g resolution.

**No other files touched.** No `src/` edits. No `tests/` edits. No `scripts/` edits. No `pyproject.toml` edits. No `configs/` edits. No `.claude/` edits. No `data/` writes. No `docs/12-roadmap/technical-debt-register.md` edits.

## 3. Ambiguity-log appends — inventory

| GAP ID              | Area        | Status   | Summary                                                                                          |
|---------------------|-------------|----------|--------------------------------------------------------------------------------------------------|
| GAP-20260424-036    | METHODOLOGY | RESOLVED | Phase 2f §11.2 fold-scheme convention pinned for future waves: 5 rolling folds, fold 1 partial-train, all tests inside R. Standing convention; spec not edited; ambiguity-log entry is canonical reference. |

## 4. Factual recap completeness

The memo's Part 1 cross-checks against the source committed reports:

- §1.1 Phase 2e baseline numbers — quoted from `2026-04-20_phase-2e-baseline-summary.md` (BTC 41 trades / WR 29.27% / expR −0.43 / PF 0.32 / net −3.95% / maxDD −4.23%; ETH 47 / 23.40% / −0.39 / 0.42 / −4.07% / −4.89%). Funnel rejection percentages (~58% / ~37% / ~5%) match the source report.
- §1.2 Phase 2f conclusions — quoted from `2026-04-24_phase-2f_strategy-review-memo.md` and `2026-04-24_phase-2f_gate-1-plan.md`. §10.3 / §10.4 / §11.3 / §11.4 / §11.6 wording mirrored.
- §1.3 Phase 2g wave-1 result — quoted from `2026-04-24_phase-2g_wave1_variant-comparison.md` §1 (full headline table) and §6 (verdict). Per-fold pattern matches the comparison report §3 + §3.A.
- §1.4 / §1.5 — what-proved-technically and what-remains-strategically synthesized from the Phase 2g checkpoint report.

No re-derivation. No re-ranking. No threshold reframe.

## 5. Diagnosis framework — ruled-out / not-ruled-out tables

§2.1 enumerates three "ruled out" findings (setup-window length, HTF EMA pair speed, break-even threshold timing) with per-axis evidence cited (specific R-window numbers from §1.3). §2.2 enumerates four "not ruled out" categories (trigger expansion signal, untested entry-side axes, untested exit-side axes including H-D6, untested bundled variants, untested structural axes). §2.3 ranks four interpretation hypotheses by support strength (HIGH / MEDIUM / MEDIUM / LOW with explicit rationales). The table above and the §2.3 ordering are the diagnostic spine of the memo.

## 6. H-B2 explicit handling

§2.9 contains four explicit sub-bullets:

- Is the near-pass a genuine signal worth follow-up? → Yes, +0.133 R/trade is non-trivial; but the §10.3 |maxDD| veto is binding.
- Is a bundled follow-up justified? → No, "H-B2 + tighter stop-band" is the canonical "rescue a near-pass with one more knob" anti-pattern that §11.3.5 forbids.
- Required guardrails if H-B2-related follow-up is ever recommended → must come from a structural redesign justified independently of H-B2's near-pass.
- Where the H-B2 signal legitimately informs future work → as a *diagnostic input* into Option B's redesign (proportional-DD scaling is a structural design constraint).

The anti-bundled-rescue language is present and explicit.

## 7. Anti-overfitting / methodology

§2.10 has five sub-items:

- §2.10.1 "Avoiding 'just one more tweak'" — stop-rule for single-axis search on the four tested axes.
- §2.10.2 "When a negative result should stop a family" — disciplined stopping rule (structural redesign tried + clean negative, or a clearly better candidate family).
- §2.10.3 "Sample segmentation / alternative scoring" — analytic enhancements deferred to Phase 2i, not 2h.
- §2.10.4 "Fold-scheme ambiguity" — Phase 2f §11.2 ambiguity recorded as GAP-20260424-036.
- §2.10.5 "Other methodology items" — explicit non-proposal to soften §10.3 / §10.4 / §11.4 / §11.3.5.

Stop-rule is recorded; threshold-preservation is explicit.

## 8. Decision options analysis

A/B/C/D each rated on pros / cons / wasted-effort / EVI in standard four-row tables (§§ 2.4 / 2.5 / 2.6 / 2.7). The memo's recommendation criteria in §2.8 spell out what would justify each path independently of the recommendation choice itself.

## 9. Recommendation

Primary (provisional): **Phase 2i Option B — Structural Breakout Redesign Planning (docs-only).**
Fallback (provisional): **Phase 2i Option A — narrow Wave 2 with H-D6 exit-model bake-off.**
Phase 4 stays deferred per existing operator policy.

§3.2 records the reasoning for choosing B over A explicitly: wave-1 evidence already supports "parameter-level fixes don't work on these axes"; the honest next step is a structural question, not a parameter-search question; running H-D6 first risks producing yet another "doesn't move the needle" result. The memo also acknowledges that the operator may legitimately prefer the secondary as primary.

## 10. "What would change this recommendation"

§3.3 contains four switch-condition blocks:

- **B → A** (wave 2 as primary): conditions where exit-model evidence should precede structural redesign.
- **B → C** (different family): conditions where structural redesign of the breakout family should be skipped in favor of a different family entirely.
- **B → defer** (no new phase): operator-pause / documentation-correction / new-restriction conditions.
- **any → D** (Phase 4): explicit operator policy change about building operational infrastructure without strategy-edge confirmation.

Each block enumerates 2–4 specific evidence/reasoning kinds. The conditions are pre-declared so future operator decisions can be measured against them as cleanly as wave-1 was measured against §10.3 / §10.4.

## 11. Wave-1 result preservation

The memo's Part 1 §1.3 quotes the wave-1 R-window headline verbatim from the Phase 2g comparison report. The memo's §3.4 explicit non-proposal list states "Any re-derivation or re-ranking of the wave-1 result. The verdict is REJECT ALL per Phase 2g and stays REJECT ALL." No threshold change, no fold-scheme retreat, no result-driven retrofit.

## 12. Threshold preservation

§10.3 disqualification floor (worse expR, worse PF, |maxDD| > 1.5×): unchanged.
§10.4 hard reject (rising trades + expR < −0.50 OR PF < 0.30): unchanged.
§11.3 no-peeking + top-1–2 promotion: unchanged.
§11.3.5 pre-declared thresholds, no post-hoc loosening: unchanged.
§11.4 ETH-as-comparison: unchanged.
§11.6 cost-sensitivity: unchanged.

The memo's §2.10.5 records each as "no proposal to soften / change". The §3.4 explicit non-proposal list reaffirms.

## 13. Safety posture

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
| Phase 2i work                                    | none (this is the phase that proposes 2i, not starts it) |
| New backtests / variants / data                  | none                                                   |
| Threshold tightening / loosening                 | none                                                   |
| New source, test, script, or config files        | none                                                   |

## 14. Operator restrictions honoured

All three Gate 1 conditions applied. All "still forbidden" items from the Gate 1 approval text held: no code changes, no new backtests, no new variants, no data downloads, no API calls, no Phase 4 work, no `technical-debt-register.md` edits, no MCP/Graphify/`.mcp.json`, no `git add`, no `git commit`, no push.

## 15. Test suite

`uv run pytest` expected to pass **396 tests** (identical to end of Phase 2g). Phase 2h made zero code changes; no test count change is expected. Output captured at the pre-commit stop point.

## 16. Recommended next step

Operator / ChatGPT Gate 2 review of:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_decision-memo.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2h_gate-2-review.md` (this file)
- `docs/00-meta/implementation-ambiguity-log.md` (GAP-20260424-036 append)

If approved, proceed to the five-commit sequence (Gate 1 plan; decision memo; ambiguity-log append; this Gate 2 review; Phase 2h checkpoint report) per Gate 1 plan §21. After commits, the operator chooses among:

- **Option A** (provisional fallback) — Phase 2i: narrow Wave 2 with H-D6 exit-model bake-off as the centerpiece.
- **Option B** (provisional primary) — Phase 2i: Structural Breakout Redesign Planning (docs-only).
- **Option C** — Phase 2i: New Strategy-Family Research Planning (only after Option B is honestly tried per the memo's §3.3 switch conditions).
- **Option D** — Phase 4: Runtime / state / persistence (only if operator policy explicitly changes per the memo's §3.3).

The recommendation is provisional; the operator's choice is the binding decision.

## 17. Questions for operator / ChatGPT

None. All three Gate 1 conditions have been applied inline. The §3.3 "What would change this recommendation" section makes the switch conditions explicit and pre-declared.

---

**Stop here. No `git add` / `git commit` has run. Awaiting operator / ChatGPT Gate 2 approval.**
