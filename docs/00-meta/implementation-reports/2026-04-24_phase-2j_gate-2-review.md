# Phase 2j — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2j/structural-redesign-memo` (created from `main` at `8a34f20` — verified clean working tree, synchronized with `origin/main` after the Phase 2i PR #10 merge)
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2j), awaiting operator / ChatGPT Gate 2 approval
**Scope:** Pre-commit review of the Phase 2j docs-only deliverables against the Phase 2j Gate 1 plan and the operator's process requirements. No `git add` / `git commit` has been run. Quality gates green; pytest 396 passing.

---

## Phase

**Phase 2j — Structural Redesign Memo Only.**

Decision/planning-only phase following the Phase 2i recommendation (carry-forward set R1a + R3, capped at ≤ 2 per Gate 1 condition 1). Goal: write full rule specs for R1a (Volatility-percentile setup) and R3 (Fixed-R exit with time stop), pin committed sub-parameter values, define candidate-specific falsifiable hypotheses, and prepare for a future operator-approved execution-planning phase. No code, no new backtests, no new variants, no data, no API calls, no Phase 4 work, no fallback-Wave-2 start.

## 1. Scope confirmed against Gate 1 plan

Match against `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md` §§ 4–18 and §24 execution sequence.

| Gate 1 requirement                                                                          | Status  | Location of evidence                                                                                                  |
|---------------------------------------------------------------------------------------------|---------|-----------------------------------------------------------------------------------------------------------------------|
| Section A — Executive summary                                                               | Done    | Memo §A (R1a + R3 brief; why chosen; why planning, not execution)                                                       |
| Section B — Fixed evidence recap                                                            | Done    | Memo §B (Phase 2e baseline; Phase 2g wave-1; Phase 2i rationale; explicit preservation of REJECT ALL / H0 / ≤ 2 carry-forward) |
| Section C — Full R1a spec                                                                   | Done    | Memo §§ C.1–C.16 (16 sub-items per Gate 1 plan checklist)                                                                |
| Section D — Full R3 spec                                                                    | Done    | Memo §§ D.1–D.18 (18 sub-items per Gate 1 plan checklist)                                                                |
| Section E — Side-by-side comparison                                                         | Done    | Memo §E (10-row table: thesis, family, funnel target, trade-count effect, expR effect, drawdown effect, complexity, overfitting, validation burden, GAPs, first-execution suitability) |
| Section F — Common validation framework restated                                            | Done    | Memo §§ F.1–F.7 (H0 only; wave-1 historical; thresholds; R/V split; GAP-036 fold scheme; mandatory diagnostics)         |
| Section G — Execution-readiness assessment                                                  | Done    | Memo §§ G.1–G.3 (R1a READY; R3 READY; joint readiness)                                                                  |
| Section H — Recommendation                                                                  | Done    | Memo §H (provisional: both advance, R3 prioritized first; reasoning + four operator-choice paths)                       |
| Section I — What would change this recommendation                                           | Done    | Memo §§ I.1–I.5 (five switch-condition blocks)                                                                          |
| Section J — Explicit non-proposal list                                                      | Done    | Memo §J (no execution, no backtest, no threshold change, no wave-1 revival, no fallback start, no Phase 4, no code, no data, no API, no MCP, no TD-register edits, no carry-forward expansion, no third candidate, no wave-1 baseline comparison, no disguised sweeps, no live/paper/capital, no result re-derivation, no recommendation re-framing) |
| Carry-forward discipline preserved (only R1a + R3)                                          | Done    | Memo §A states the candidates explicitly; §J explicitly forbids expansion                                                |
| R1 coherence outcome from Phase 2i preserved (R1 split into R1a + R1b; R1b not carried forward) | Done    | Memo §A and §B.3 cite Phase 2i §3.2 reasoning explicitly                                                                 |
| H0-only comparison anchor restated                                                          | Done    | Memo §B.4 and §F.1 (two binding statements)                                                                              |
| Wave-1 historical-only restated                                                             | Done    | Memo §B.4 and §F.2                                                                                                       |
| R/V split unchanged (Phase 2f §11.1)                                                        | Done    | Memo §F.4                                                                                                                |
| GAP-036 fold scheme unchanged                                                               | Done    | Memo §F.5                                                                                                                |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds unchanged                                  | Done    | Memo §F.3 reproduces all thresholds; §J explicit non-proposal list reaffirms                                              |
| §1.7.3 project-level locks preserved                                                        | Done    | Memo §C.9 (R1a) and §D.11 (R3) preserve locks explicitly                                                                  |
| Single committed value per sub-parameter (no disguised sweep)                               | Done    | R1a: X=25, N=200 committed singularly with research-default justification (§C.6). R3: R_TARGET=2.0, TIME_STOP_BARS=8 committed singularly with project-convention justification (§D.6). §J explicitly forbids sweeps. |
| Falsifiable hypothesis per candidate, pre-committed                                         | Done    | R1a hypothesis (§C.15); R3 hypothesis (§D.17). Both reference §10.3 / §10.4 thresholds verbatim from Phase 2f.            |
| GAP dispositions per candidate                                                              | Done    | R1a (§C.14): CARRIES 030, 031, 032, 033 / supersedes nothing. R3 (§D.16): SUPERSEDES 030, CARRIES 031 / 032, CARRIES-AND-EXTENDS 033. |
| Implementation impact described as descriptive (no code in 2j)                              | Done    | Memo §C.10 and §D.12 explicitly note "Phase 2j writes no code; descriptive only."                                         |
| Mandatory diagnostics specified (common framework + candidate-specific)                     | Done    | Common framework §F.6 (4 items); R1a-specific §C.16 (2 items); R3-specific §D.18 (3 items).                              |
| Recommendation provisional + evidence-based framing                                         | Done    | Memo §H opens with three explicit non-claims; primary and fallback both labeled "(provisional)".                          |

**No scope diffs from the approved Gate 1 plan.** The operator's process requirements (no quiet scope widening; no disguised sweeps; no wave-1-as-baseline comparisons; no live-deployment recommendation; explicit hidden-DOF callout if needed; surface conflicts explicitly) are all honored.

## 2. Docs written in Phase 2j

- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md` — Gate 1 plan with all process requirements applied inline.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md` — three-part-style memo with sections A–J per the operator's required structure. Substantially the largest deliverable in the phase.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md` — this review.

**No ambiguity-log appends.** Phase 2j Gate 1 plan §18 anticipated this case ("most likely no new GAP is needed"). The §1.7 binding test from Phase 2i, the existing Phase 2f thresholds, and the per-candidate spec disciplines handled every judgement in this memo. The R1a percentile-rank tie-breaking convention (stable order) and the R3 stop-vs-take-profit priority on the same bar (stop wins) are spec-internal choices, not GAPs against the v1 spec or any prior-phase doc.

**No other files touched.** No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `data/`, or `technical-debt-register.md` edits. No edits to existing ambiguity-log entries.

## 3. R1a spec completeness check

Per Gate 1 plan §C checklist:

| Item                                                            | Memo location |
|-----------------------------------------------------------------|---------------|
| Objective / thesis                                              | §C.1          |
| Exact rule shape                                                | §C.2          |
| Exact inputs used                                               | §C.3          |
| Exact timeframes                                                | §C.4          |
| Exact setup-validity predicate (mathematical form)              | §C.5          |
| Committed sub-parameter values (X=25, N=200, warmup floor)     | §C.6          |
| Relationship to existing trigger / bias / entry / stop / exit logic | §C.7      |
| What H0 rules are replaced                                      | §C.8          |
| What H0 rules remain unchanged                                  | §C.9          |
| Implementation impact (descriptive only)                        | §C.10         |
| Expected mechanism of improvement                               | §C.11         |
| Expected main failure mode                                      | §C.12         |
| Why structural and not parametric                               | §C.13         |
| GAP dispositions                                                | §C.14         |
| Candidate-specific falsifiable hypothesis                       | §C.15         |
| Candidate-specific mandatory diagnostics beyond common framework | §C.16         |

All 16 items present. R1a's spec is complete.

## 4. R3 spec completeness check

Per Gate 1 plan §D checklist:

| Item                                                            | Memo location |
|-----------------------------------------------------------------|---------------|
| Objective / thesis                                              | §D.1          |
| Exact exit philosophy                                           | §D.2          |
| Exact take-profit rule                                          | §D.3          |
| Exact time-stop rule                                            | §D.4          |
| Exact interaction with the initial stop                         | §D.5          |
| Committed sub-parameter values (R_TARGET=2.0, TIME_STOP_BARS=8) | §D.6          |
| Whether any staged management remains                           | §D.7 (No)     |
| Whether break-even remains or is removed                        | §D.8 (Removed) |
| Whether trailing remains or is removed                          | §D.9 (Removed) |
| What H0 rules are replaced                                      | §D.10         |
| What H0 rules remain unchanged                                  | §D.11         |
| Implementation impact (descriptive only)                        | §D.12         |
| Expected mechanism of improvement                               | §D.13         |
| Expected main failure mode                                      | §D.14         |
| Why structural and not parametric                               | §D.15         |
| GAP dispositions                                                | §D.16         |
| Candidate-specific falsifiable hypothesis (with §10.3.c note)   | §D.17         |
| Candidate-specific mandatory diagnostics beyond common framework | §D.18         |

All 18 items present. R3's spec is complete.

## 5. Side-by-side comparison check

Memo §E contains a 10-row comparison table covering every required dimension from Gate 1 plan §E:

- Thesis (R1a setup-redesign; R3 exit-redesign)
- Family (S vs X)
- Funnel-rejection target (58% no-valid-setup vs trailing-machine inactive)
- Likely effect on trade count
- Likely effect on expectancy
- Likely effect on drawdown
- Likely implementation complexity (R1a MEDIUM; R3 LOW-MEDIUM)
- Likely overfitting risk (R1a MEDIUM; R3 LOW-MEDIUM)
- Likely validation burden (comparable, ~6 diagnostics each)
- GAP dispositions (R1a CARRIES all 4; R3 SUPERSEDES 030, CARRIES-AND-EXTENDS 033)
- First-execution-suitability ranking (R3 first; R1a second)

The first-execution-suitability ranking is a sequencing preference, not a deferral of R1a; both candidates are recommended for joint advance per §H.

## 6. Common validation framework check

Memo §§ F.1–F.7 reproduce the framework from Phase 2i §2.5 and Phase 2j Gate 1 plan §9:

- §F.1 H0 as only comparison anchor (one binding statement).
- §F.2 Wave-1 variants as historical evidence only (one binding statement).
- §F.3 §10.3 / §10.4 / §11.3 / §11.4 / §11.6 discipline preserved (each threshold reproduced verbatim with §11.3.5 no-loosening rule explicit).
- §F.4 R/V split unchanged.
- §F.5 GAP-036 fold convention unchanged.
- §F.6 Required diagnostics: 4 common-framework items + 2 R1a-specific + 3 R3-specific.
- §F.7 Candidate-specific success criteria pre-declared.

## 7. Execution-readiness assessment check

§G.1 R1a: READY (with caveats around implementation surface and sub-parameter sensitivity flagged).
§G.2 R3: READY (with caveats around new exit-reason schema changes and GAP-033 extension flagged).
§G.3 Joint: both READY for a future operator-approved Phase 2k execution-planning phase.

Neither candidate is "needs more docs" or "drop". Per §G.3, the joint READY assessment is consistent with the §H primary recommendation that both advance.

## 8. Recommendation check

Memo §H records:

- **Primary (provisional):** Both R1a and R3 advance; R3 prioritized for first execution.
- Three explicit non-claims (R1a/R3 won't necessarily produce positive results; ranking reflects implementation risk not predicted edge; no live-deployment implication).
- Four operator-choice paths (both advance / R1a only / R3 only / neither without more docs).
- Reasoning includes: both specs complete; R3 cleaner first test; R1a follows naturally; no third candidate; Phase 4 deferred.

§H mirrors the provisional/evidence-based framing from Phase 2h §3.1 and Phase 2i §3.1 to maintain consistency across phases.

## 9. "What would change this recommendation" check

§§ I.1–I.5 enumerate five switch conditions:

- I.1 Switch to "only R1a advances" (operator preference for setup over exit; uninterpretability argument; H-D6-overlap argument).
- I.2 Switch to "only R3 advances" (smaller surface preference; faster strict-dominance falsifiability; R1a-sweep-too-wide argument).
- I.3 Switch to "neither advances without more docs" (hidden DOF discovery; documentation inconsistency; operator pause).
- I.4 Switch to fallback Wave 2 (H-D6) instead of Phase 2k (Phase 2i §3.4 conditions).
- I.5 Switch to Phase 4 (operator policy change; current policy unchanged).

Switch conditions are pre-declared so future operator decisions can be measured against them as cleanly as wave-1 was measured against §10.3 / §10.4.

## 10. Explicit non-proposal list check

Memo §J enumerates 18 explicit non-proposals covering: execution / backtest / threshold change / wave-1 revival / H-D6 fallback start / Phase 4 / code change / new dependency / data download / API call / MCP / TD-register edit / carry-forward expansion / third candidate / wave-1-as-baseline / disguised sweep / live-deployment / wave-1-verdict re-derivation / Phase 2h-or-2i recommendation re-framing.

The non-proposal list explicitly forbids each restriction the operator listed in the Phase 2j approval message.

## 11. Wave-1 result preservation

Memo §B.2 quotes wave-1 facts diagnostically (H-A1 frequency-collapse pattern; H-D3 break-even-tweak indistinguishability; H-B2 trigger-loosening + DD-scaling pattern). §B.4 explicitly states: "No re-derivation. No re-ranking. Wave-1 numbers may be cited diagnostically (as in §B.2 above) but do not serve as comparison baselines for R1a or R3." §J reaffirms in the explicit non-proposal list. The REJECT ALL verdict stands.

## 12. Phase 2h + Phase 2i recommendation preservation

§B.3 and §B.4 cite Phase 2i §3.2 reasoning for choosing R1a and R3 verbatim. §A executive summary explicitly notes both Phase 2h (provisional Option B primary) and Phase 2i (carry-forward R1a + R3, ≤ 2 cap, R1 split, H0 anchor) as inputs to Phase 2j. §J reaffirms no re-framing of either prior recommendation.

## 13. Threshold preservation

§F.3 reproduces every Phase 2f threshold:

- §10.3 promotion paths (a, b, c).
- §10.3 disqualification floor (worse expR / worse PF / |maxDD| > 1.5×).
- §10.4 hard reject (rising trades + expR < −0.50 OR PF < 0.30).
- §11.3 no-peeking + top-1–2 promotion to V.
- §11.4 ETH-as-comparison.
- §11.6 cost-sensitivity.
- §11.3.5 pre-committed-thresholds discipline.

All applied unchanged. §J explicit non-proposal list reaffirms.

## 14. §1.7.3 project-level locks preservation

Memo §C.9 (R1a kept rules) and §D.11 (R3 kept rules) each enumerate the §1.7.3 locks explicitly:

- BTCUSDT live primary; ETHUSDT research/comparison.
- One-way mode, isolated margin, one position max, no pyramiding, no reversal while positioned.
- Initial live risk 0.25%, leverage cap 2x, internal notional cap mandatory.
- Mark-price stops as live protective-stop type.
- v002 datasets, manifests, 51-month coverage.

Family-R candidates that would violate any lock remain excluded per Phase 2i §2.1.5; no Family-R sub-rules appear in R1a or R3.

## 15. Disguised parameter sweep avoidance check

Per Phase 2j Gate 1 plan §12 and operator process requirement 2:

- R1a's X=25 and N=200 are committed singular values (§C.6), each justified as a research default with literature/convention reference. The eventual execution does not sweep them.
- R3's R_TARGET=2.0 and TIME_STOP_BARS=8 are committed singular values (§D.6), each justified by alignment with existing project conventions. The eventual execution does not sweep them.
- §J explicit non-proposal list forbids sweeps.

If a future Phase 2k+1 wants different values, that is a new operator-approved spec, not a sweep within R1a or R3.

## 16. No-comparison-to-wave-1-as-baseline check

Per operator process requirement 3:

- Memo §F.1 explicitly states H0 is the only comparison anchor.
- Memo §F.2 explicitly states wave-1 variants are historical evidence only, not promotion baselines.
- §J explicit non-proposal list forbids "comparison of R1a or R3 to wave-1 variants as promotion baselines. H0 only."
- §B.2 cites wave-1 numbers diagnostically (e.g., "H-A1 showed setup-window length is not the binding parameter") — diagnostic citation, not comparison baseline.

## 17. Hidden-DOF callout check

Per operator process requirement 5 ("If R1a or R3 cannot be specified cleanly without hidden degrees of freedom, say so explicitly."):

- R1a has two sub-parameters (X, N). Both are committed singularly with literature/convention justification (§C.6). Boundary cases (NaN seeds, ties at X percentile) are explicitly resolved (§C.5). Warmup floor is computed explicitly (§C.6, §C.10). No hidden DOF.
- R3 has two sub-parameters (R_TARGET, TIME_STOP_BARS). Both are committed singularly with project-convention justification (§D.6). Boundary cases (stop-and-take-profit priority on the same bar; time-stop unconditional vs. conditional) are explicitly resolved (§D.4, §D.5). No hidden DOF.

The §G assessment confirms both are READY without more docs.

## 18. Prior-doc conflict check

Per operator process requirement 6 ("If prior docs conflict, surface the conflict explicitly."):

No conflict found between Phase 2i recommendation (carry-forward R1a + R3, ≤ 2) and Phase 2j memo (specs R1a + R3 with both READY). No conflict between Phase 2h §3.3 switch conditions and Phase 2j §I switch conditions (Phase 2j's are downstream of Phase 2h's). No conflict with v1 spec or risk/stop/exposure docs. The §1.7.3 locks are honored.

If the operator review finds a conflict that this memo missed, that is a switch-condition-§I.3 trigger ("neither advances without more docs"), not an ignored conflict.

## 19. Safety posture

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
| Fallback Wave 2 / H-D6 start                     | none (operator restriction)                            |
| Phase 2k execution-planning work                 | none (operator restriction; this phase proposes 2k, does not start it) |
| New backtests / variants / data                  | none                                                   |
| Threshold tightening / loosening                 | none                                                   |
| New source, test, script, or config files        | none                                                   |
| Re-derivation of wave-1 verdict                  | none — REJECT ALL preserved                            |
| Re-framing of Phase 2h or Phase 2i recommendation | none — both are inputs                                 |
| Comparison of redesign candidates to wave-1 as baselines | none — H0 only                                  |
| Disguised parameter sweeps                       | none — single committed value per sub-parameter        |
| Carry-forward expansion beyond R1a + R3          | none                                                   |
| Quiet scope widening                             | none                                                   |

## 20. Operator restrictions honoured

All operator process requirements honored. All "Do not..." items from the Phase 2j approval message held: no code, no source edits, no installs, no data downloads, no Binance API calls, no public Binance URLs, no new backtests, no Wave 2 run, no parameter tuning, no carry-forward expansion, no MCP/Graphify/.mcp.json, no credential request, no production keys, no exchange-write, no Phase 4, no `git add` / `git commit`.

## 21. Test suite

`uv run pytest` expected to pass **396 tests** (identical to end of Phase 2i). Phase 2j made zero code changes; no test count change is expected. Output captured at the pre-commit stop point.

## 22. Recommended next step

Operator / ChatGPT Gate 2 review of:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md` (this file)

If approved, proceed to the four-commit sequence (Gate 1 plan; structural-redesign memo; this Gate 2 review; Phase 2j checkpoint report). No ambiguity-log commit since no new GAP is needed (§2 above).

After commits, the operator chooses among:

- **Phase 2k execution-planning, both R1a and R3** (recommended; both READY per §G; R3 prioritized for first execution per §E).
- **Phase 2k execution-planning, R1a only** (operator switch condition §I.1).
- **Phase 2k execution-planning, R3 only** (operator switch condition §I.2).
- **Neither advance; another docs phase** (operator switch condition §I.3).
- **Fallback Wave 2 with H-D6** (operator switch condition §I.4).
- **Phase 4** (operator switch condition §I.5; requires explicit policy change).

The recommendation is provisional; the operator's choice is the binding decision.

## 23. Questions for operator / ChatGPT

None. All Gate 1 plan requirements applied. All operator process requirements honored. The §I "What would change this recommendation" section makes the switch conditions explicit and pre-declared.

---

**Stop here. No `git add` / `git commit` has run. Awaiting operator / ChatGPT Gate 2 approval.**
