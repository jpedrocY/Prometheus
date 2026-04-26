# Phase 2k — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2k/redesign-execution-planning` (created from `main` at `c078eaa` — verified clean working tree, synchronized with `origin/main` after the Phase 2j PR #11 merge)
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2k), awaiting operator / ChatGPT Gate 2 approval
**Scope:** Pre-commit review of the Phase 2k docs-only Gate 1 plan against the operator's brief and the Phase 2j hand-off contract. No `git add` / `git commit` has been run. Quality gates green; pytest 396 passing.

---

## Phase

**Phase 2k — Structural Redesign Execution Planning.** Decision/planning-only phase following the Phase 2j memo §H provisional recommendation (both R1a + R3 advance; R3 prioritized for first execution). Goal: plan exactly how R1a and R3 would be executed against v002 datasets under the unchanged Phase 2f validation framework, without writing code or running anything. The Gate 1 plan IS the substantive planning artifact — no separate execution-planning memo. After Gate 1 approval (granted), only this Gate 2 review and the checkpoint report remain to draft.

## 1. Scope confirmed against Gate 1 plan

Match against `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-1-plan.md` §§ 6–19 (the substantive content) and §§ 23–30 (governance, output artifacts, post-approval execution sequence).

| Operator brief requirement                                                                            | Status  | Location of evidence in Gate 1 plan                                                                       |
|-------------------------------------------------------------------------------------------------------|---------|-----------------------------------------------------------------------------------------------------------|
| Executive summary                                                                                     | Done    | §1                                                                                                        |
| Plain-English explanation                                                                             | Done    | §2                                                                                                        |
| Current branch/status verification commands                                                           | Done    | §3                                                                                                        |
| Proposed Phase 2k branch name                                                                         | Done    | Header + §3 + §30 ("phase-2k/redesign-execution-planning")                                                  |
| Exact scope                                                                                           | Done    | §4                                                                                                        |
| Explicit non-goals                                                                                    | Done    | §5 (~22 explicit non-goals)                                                                                |
| Fixed evidence recap (R1a READY / R3 READY / R3 first / what unchanged from 2f/2g/2i/2j)              | Done    | §§ 6.1–6.4                                                                                                |
| Execution-order analysis (≥ 4 options)                                                                | Done    | §§ 7.1–7.4 (4 options: R3-first sequential / R1a-first sequential / both-in-one / one-only-other-deferred) with pros / cons / contamination / wasted-effort / EVI per option, plus §7.5 comparison summary |
| Recommended execution order with explicit reasoning                                                   | Done    | §8 (R3 first, then R1a, sequential — Option 1 in §7.1; six-point reasoning)                               |
| Implementation-scope planning per candidate (config / strategy / backtester / diagnostics / tests / scripts / report schema / exit-reason taxonomy) | Done    | §§ 9.1 (R3) + 9.2 (R1a) cover all required surfaces; §9.3 reusable scaffolding; §9.4 minimal-implementation; §9.5 H0 bit-for-bit preservation requirement |
| Required R3 forwarding notes (same-bar priority STOP > TAKE_PROFIT; new exit reasons; same Phase 2f framework; §10.3.c additional path not framework rewrite) | Done    | §10 reproduces all four items verbatim from operator's Phase 2j non-blocking note                         |
| Required R1a execution notes (8-bar window remains; percentile replaces setup-validity only; X=25 / N=200 singular not sweep; warmup floor explicit; funnel attribution interpretable) | Done    | §11 reproduces all five items verbatim from operator's Phase 2k brief                                     |
| Execution-plan structure (one phase combined vs. one candidate at a time / reusable scaffolding / minimal-implementation / H0 bit-for-bit preservation) | Done    | §§ 12.1–12.4                                                                                              |
| Report-contract planning                                                                              | Done    | §§ 13.1–13.6 (per-symbol artifacts; candidate-specific outputs; common diagnostics; committed comparison report layout; H0 comparison presentation; R/V and fold separation) |
| Validation framework restatement (H0 only anchor / wave-1 historical only / §10.3 etc unchanged / R/V split / GAP-036 fold / no post-hoc loosening) | Done    | §§ 14.1–14.6                                                                                              |
| Execution-readiness risks (per-candidate failure modes + stop-and-escalate triggers)                   | Done    | §§ 15.1 (R1a) + 15.2 (R3) + 15.3 (stop-and-escalate)                                                      |
| Relationship to fallback paths (when H-D6 supersedes / when Phase 4 stays deferred / when docs phase preferable) | Done    | §§ 16.1–16.3                                                                                              |
| Proposed next-phase options after 2k (≥ 5: Option A R3 sequential / B both-in-one / C docs phase / D H-D6 / E Phase 4) with pros / cons / wasted-effort / EVI | Done    | §17 (5 options compared)                                                                                  |
| Final recommendation (primary + fallback + reasoning)                                                 | Done    | §18 (provisional primary Option A; provisional fallback Option B; six-point reasoning)                     |
| "What would change this recommendation" with switch conditions                                        | Done    | §§ 19.1–19.6 (six switch-condition blocks)                                                                |
| Proposed files / directories                                                                          | Done    | §20 (Gate 1 plan; Gate 2 review; checkpoint report; no separate memo)                                      |
| No code changes in 2k                                                                                 | Done    | §21 explicit                                                                                              |
| No dependency additions                                                                               | Done    | §21 explicit                                                                                              |
| Output artifact plan                                                                                  | Done    | §22                                                                                                       |
| Safety constraints                                                                                    | Done    | §23 (~28 items)                                                                                           |
| Ambiguity / spec-gap items to log                                                                     | Done    | §24 (no new GAP anticipated; conditional GAP-037 if surfaces)                                              |
| TD-register items affected                                                                            | Done    | §25 (no edits; TD-016 informationally affected by future execution results)                                |
| Proposed commit structure                                                                             | Done    | §26 (3 commits: Gate 1 plan; Gate 2 review; checkpoint report)                                             |
| Gate 2 review format                                                                                  | Done    | §27 (template provided)                                                                                   |
| Checkpoint report format                                                                              | Done    | §28 (workflow template referenced)                                                                        |

**No scope diffs from the operator's brief.** All 14 required content sections + standard governance items are present in the Gate 1 plan.

## 2. Operator brief planning requirements check

Per the operator's Phase 2k brief "Important planning requirements":

1. **"Do not assume both candidates must automatically be implemented together."** Honored: §7 compares 4 options including sequential paths and one-only-other-deferred.
2. **"Do not assume R3-first is automatically correct without comparing alternatives."** Honored: §7 compares R3-first AND R1a-first AND both-in-one AND one-only with pros/cons/EVI per option; §8's recommendation is reasoned, not asserted.
3. **"Do not widen the scope beyond R1a and R3."** Honored: §5 explicit non-goal "No expansion of the carry-forward set beyond R1a + R3"; §17 next-phase options stay within R1a + R3 + fallback paths only.
4. **"Do not quietly turn committed values into sweep ranges."** Honored: §5 explicit non-goal forbids sweeps; §11 R1a notes preserve "X=25 and N=200 are single committed values, not sweep ranges"; §15.3 stop-and-escalate triggers on any sweep proposal.
5. **"Do not recommend live deployment, paper/shadow readiness, or capital increase."** Honored: §18 recommendation framing explicitly excludes any live-deployment claim; §23 safety constraints includes "no live deployment, paper/shadow readiness, or capital exposure proposal".
6. **"If prior docs conflict, surface the conflict explicitly."** Honored: header note surfaces the operator-brief vs. on-disk filename inconsistency (`scripts/phase2g_wave1_variants.py` brief vs. `scripts/phase2g_variant_wave1.py` actual). No other prior-doc conflicts found during Phase 2k planning.

## 3. Docs written in Phase 2k

- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-1-plan.md` — Gate 1 plan with all 14 required content sections per the operator's brief plus the standard governance items.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-2-review.md` — this review.

**No ambiguity-log appends.** Phase 2k Gate 1 plan §24 anticipated this case: "no new GAP anticipated"; §15 anticipates that no real ambiguity will surface during Gate 2 review. The operator-brief vs. on-disk filename inconsistency surfaced in the header is a docs-cleanup observation, not a v1-spec ambiguity that requires a permanent GAP entry. No new judgement required new infrastructure.

**No other files touched.** No `src/` edits. No `tests/` edits. No `scripts/` edits. No `pyproject.toml` edits. No `configs/` edits. No `.claude/` edits. No `data/` writes. No `docs/12-roadmap/technical-debt-register.md` edits. No edits to existing ambiguity-log entries.

## 4. Carry-forward discipline preservation

| Check | Result |
|---|---|
| Only R1a and R3 in scope | Yes (§5 explicit non-goal forbids expansion; §17 next-phase options stay within R1a + R3 + fallback paths) |
| No third candidate added | Yes |
| No revival of wave-1 variants | Yes (§5 explicit non-goal) |
| Phase 2i ≤ 2 carry-forward cap respected | Yes (§§ 6.4 + §17 Option 4 explicitly notes that "drop one candidate" would require Phase 2i cap deviation) |

## 5. Sub-parameter values preservation

| Candidate | Sub-parameters | Preserved as singular? |
|---|---|---|
| R1a | X = 25 (percentile threshold) | Yes (§§ 6.1 + 11) |
| R1a | N = 200 (lookback length) | Yes (§§ 6.1 + 11) |
| R3 | R_TARGET = 2.0 | Yes (§§ 6.2 + 6.3) |
| R3 | TIME_STOP_BARS = 8 | Yes (§§ 6.2 + 6.3) |

§5 explicit non-goal forbids turning these into sweeps. §15.3 stop-and-escalate triggers on any sweep proposal during execution. §11 R1a notes restate the singular-value commitment verbatim from the operator brief.

## 6. Execution-order analysis completeness

§7 compares all four options the operator's brief required:

| Option | Section | Pros | Cons | Contamination risk | Wasted-effort risk | EVI |
|---|---|---|---|---|---|---|
| 1 — R3 first, then R1a (sequential) | §7.1 | Smaller surface; sequential evidence; same Phase 2g pattern | 2× phase-init; slower wall-clock | LOW | LOW | HIGH |
| 2 — R1a first, then R3 (sequential reverse) | §7.2 | Targets dominant funnel rejection first | Larger up-front surface | LOW | MEDIUM | MEDIUM |
| 3 — Both in one phase, run independently | §7.3 | Single phase-init; shared scaffolding | Larger surface; harder Gate 2 review | MEDIUM | LOW-MEDIUM | MEDIUM-HIGH |
| 4 — One only, other deferred | §7.4 | Most cautious | Defers the deferred candidate; requires Phase 2i cap deviation | LOW | LOW (implemented) / HIGH (deferred) | MEDIUM |

§7.5 comparison summary table consolidates the four options on surface size, sequential-evidence availability, phase-init cost, and best-when scenario. §8 recommendation chooses Option 1 with explicit six-point reasoning.

## 7. R3 forwarding notes preservation

§10 reproduces all four items from the operator's Phase 2j non-blocking note verbatim:

- ✓ Same-bar priority: STOP over TAKE_PROFIT.
- ✓ New exit reasons: TAKE_PROFIT and TIME_STOP.
- ✓ R3 remains under the same Phase 2f framework.
- ✓ §10.3.c is an additional strict-dominance path if applicable, not a framework rewrite.

## 8. R1a execution notes preservation

§11 reproduces all five items from the operator's Phase 2k brief verbatim:

- ✓ The 8-bar setup window remains.
- ✓ The percentile predicate replaces only the setup-validity rule.
- ✓ X=25 and N=200 are single committed values, not sweep ranges.
- ✓ Warmup floor implications must be handled explicitly.
- ✓ Funnel attribution must remain interpretable.

## 9. Execution-plan structure

§§ 12.1–12.4 cover all four required sub-items:

- §12.1 One combined phase or one candidate at a time? → recommended one candidate at a time per §8 (Option 1 sequential).
- §12.2 Reusable scaffolding → V1BreakoutConfig extension pattern; runner-script helpers; comparison-report Python helper.
- §12.3 Minimal-implementation definition → only what's strictly needed; no opportunistic refactoring; no new dependencies; no schema migrations beyond the optional ExitReason enum extension for R3.
- §12.4 H0 bit-for-bit preservation → mandatory regression test re-running H0 on R and asserting identical trade counts / metrics.

## 10. Report-contract planning

§§ 13.1–13.6 cover the required elements:

- §13.1 Per-symbol per-variant artifacts (mirroring Phase 2g's `phase2g_variant_wave1.py` output structure).
- §13.2 Candidate-specific outputs (R1a: setup_validity_rate_per_fold + atr_percentile_distribution_at_entries; R3: exit_reason_histogram_extended + take_profit_r_multiple_distribution + time_stop_bias_diagnostic).
- §13.3 Common diagnostics (per-regime expR; MFE distribution; long/short asymmetry; GAP-032 mark-price sensitivity).
- §13.4 Committed comparison report layout per execution phase.
- §13.5 H0 comparison presentation (row 0; deltas vs. row 0; wave-1 only in separate appendix labeled not-a-comparison-baseline).
- §13.6 R/V and fold separation (R first, §10.3/§10.4 thresholds on R only; V only for promoted; per-fold breakdown computed on R only per GAP-036).

## 11. Validation framework restatement

§§ 14.1–14.6 restate Phase 2j memo §F unchanged:

- §14.1 H0 only anchor.
- §14.2 Wave-1 historical evidence only.
- §14.3 §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds unchanged with §11.3.5 binding.
- §14.4 R/V split unchanged.
- §14.5 GAP-036 fold convention unchanged.
- §14.6 No post-hoc threshold loosening.

## 12. Execution-readiness risks

§§ 15.1–15.3 cover all required dimensions:

- §15.1 R1a implementation risks: rolling cache state-leak; tie-breaking inconsistency; warmup floor regression; funnel attribution double-counting. Each with mitigation.
- §15.2 R3 implementation risks: same-bar priority bug; ExitReason validation regression; Stage 3/4/5 logic accidentally retained; initial stop accidentally moved; existing exit reasons still emitted. Each with mitigation.
- §15.3 Stop-and-escalate triggers: H0 regression failure; pytest baseline failure; sub-parameter sweep proposal; cross-candidate dependency; threshold change proposal; new ExitReason value beyond TAKE_PROFIT/TIME_STOP; project-level lock change.

## 13. Fallback relationships

§§ 16.1–16.3 cover all required dimensions:

- §16.1 When H-D6 fallback Wave 2 should still supersede redesign execution.
- §16.2 When Phase 4 should still remain deferred.
- §16.3 When a docs-only clarification phase would still be preferable.

## 14. Five-option next-phase comparison

§17 compares all five options the operator's brief required:

- Option A — Phase 2l: Execute R3 first, then decide on R1a (recommended primary).
- Option B — Phase 2l: Implement both R1a and R3, run independently in one phase (recommended fallback).
- Option C — Another docs-only clarification phase.
- Option D — Fallback Wave 2 with H-D6.
- Option E — Phase 4: Runtime / state / persistence.

Each option rated on pros / cons / wasted-effort risk / EVI.

## 15. Recommendation framing

§18 records:

- **Primary (provisional):** Option A — Phase 2l: Execute R3 first, then decide on R1a (sequential). Six-point reasoning.
- **Secondary (fallback, provisional):** Option B — Both in one phase. Reasoning explicit.
- **Phase 4 stays deferred** per existing operator policy.

The framing mirrors Phase 2h §3.1, Phase 2i §3.1, and Phase 2j §H provisional / evidence-based discipline:

- Three explicit non-claims (R3 first not permanently right; R1a/R3 may not produce positive results; not a live-deployment recommendation).
- Provisional labels on both primary and fallback.

## 16. "What would change this recommendation"

§§ 19.1–19.6 enumerate six switch-condition blocks:

- §19.1 Switch from Option A (R3-first sequential) to Option B (both in one phase).
- §19.2 Switch from Option A (R3-first) to a different sequential ordering (R1a-first).
- §19.3 Switch from Option A to Option C (another docs phase).
- §19.4 Switch from Option A to Option D (fallback Wave 2 with H-D6).
- §19.5 Switch from Option A to Option E (Phase 4).
- §19.6 Switch from Option A to "drop one candidate" (Phase 2i ≤ 2 cap deviation).

Each block enumerates specific evidence/reasoning kinds that would justify the switch. Pre-declared so future operator decisions can be measured against them.

## 17. Wave-1 result preservation

§§ 6.4 explicit non-proposal items:

- "Phase 2g wave-1 verdict (REJECT ALL). No re-derivation. No re-ranking. Wave-1 numbers may be cited diagnostically but do not serve as comparison baselines for R1a or R3."
- "Phase 2h provisional recommendation framing. Phase 2h is the input that led to Phase 2i/2j/2k. Not a target for revision."

§5 explicit non-goal: "No re-derivation or re-ranking of the wave-1 result." §23 safety constraints: "Re-derivation of wave-1 verdict — none."

## 18. Phase 2h / Phase 2i / Phase 2j recommendation preservation

§6.4 fixed evidence recap explicitly preserves all three prior recommendations as inputs:

- Phase 2h provisional recommendation framing (Option B Structural Breakout Redesign Planning, the provisional Phase 2i path).
- Phase 2i recommendation (carry-forward set R1a + R3, ≤ 2 cap, R1 split into R1a + R1b, H0 anchor).
- Phase 2j R1a + R3 specs (sub-parameter values committed singularly; falsifiable hypotheses pre-declared).

§5 explicit non-goal: "No re-framing of the Phase 2h, Phase 2i, or Phase 2j recommendations (all are inputs)." §23 safety constraints reaffirms.

## 19. Threshold preservation

§14 reproduces every Phase 2f threshold unchanged:

- §10.3 promotion paths (a, b, c).
- §10.3 disqualification floor.
- §10.4 hard reject.
- §11.3 no-peeking + top-1–2 promotion.
- §11.4 ETH-as-comparison.
- §11.6 cost-sensitivity.
- §11.3.5 pre-committed-thresholds discipline.

§5 explicit non-goal: "No tightening or loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold." §23 safety constraints reaffirms.

## 20. §1.7.3 project-level locks preservation

§6.4 + §14 preserve all locks. §5 explicit non-goal: project-level locks are off-limits. §23 safety constraints reaffirms (no risk-policy redesign; no Family-R candidate; no live-deployment-eligible exception).

## 21. Disguised parameter sweeps avoidance

| Check | Result |
|---|---|
| Single committed value per R1a sub-parameter | Yes — X=25, N=200 (§§ 6.1 + 11) |
| Single committed value per R3 sub-parameter | Yes — R_TARGET=2.0, TIME_STOP_BARS=8 (§§ 6.2 + 6.3) |
| §5 explicit non-goal forbids sweeps | Yes |
| §15.3 stop-and-escalate triggers on any sweep proposal | Yes |

## 22. Safety posture

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
| Phase 2l work                                    | none (this phase proposes 2l, does not start it)       |
| Fallback Wave 2 / H-D6 start                     | none (operator restriction)                            |
| Carry-forward expansion beyond R1a + R3          | none                                                   |
| Wave-1 variant revival                           | none                                                   |
| Sub-parameter sweeps                             | none                                                   |
| Threshold tightening / loosening                 | none                                                   |
| Re-derivation of wave-1 verdict                  | none — REJECT ALL preserved                            |
| Re-framing of Phase 2h / 2i / 2j recommendations | none — all are inputs                                  |
| Comparison of redesigns to wave-1 as baselines   | none — H0 only                                         |
| Quietly re-classifying parametric as structural  | none — Phase 2i §1.7 binding test inherited            |
| Live deployment / paper-shadow readiness         | none                                                   |

## 23. Operator restrictions honoured

All restrictions from the operator's Phase 2k Gate 1 approval honored:

- ✓ docs only
- ✓ no code changes
- ✓ no new backtests
- ✓ no execution of R1a or R3
- ✓ no data downloads
- ✓ no API calls
- ✓ no fallback H-D6 Wave 2 start
- ✓ no Phase 4 work
- ✓ no `technical-debt-register.md` edits
- ✓ no `git add` (will be done after Gate 2 approval, not now)
- ✓ no `git commit` (will be done after Gate 2 approval)
- ✓ no `git push`

## 24. Test suite

`uv run pytest` expected to pass **396 tests** (identical to end of Phase 2j). Phase 2k made zero code changes; no test count change is expected. Output captured at the pre-commit stop point.

## 25. Recommended next step

Operator / ChatGPT Gate 2 review of:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2k_gate-2-review.md` (this file)

If approved, proceed to the three-commit sequence (Gate 1 plan; this Gate 2 review; Phase 2k checkpoint report). No ambiguity-log commit since no new GAP is needed (§3 above).

After commits, the operator chooses among:

- **Phase 2l Option A (provisional primary)** — Execute R3 first, then decide on R1a (sequential).
- **Phase 2l Option B (provisional fallback)** — Implement both R1a and R3, run independently in one phase.
- **Phase 2l Option C** — Another docs-only clarification phase (operator switch condition §19.3).
- **Phase 2l Option D** — Fallback Wave 2 with H-D6 (operator switch condition §19.4).
- **Phase 2l Option E** — Phase 4 (operator switch condition §19.5; requires explicit policy change).
- **Phase 2l Option (drop one)** — Phase 2i ≤ 2 cap deviation per §19.6.

The recommendation is provisional; the operator's choice is the binding decision.

## 26. Questions for operator / ChatGPT

None. All operator brief content requirements applied; all process requirements honored; all switch conditions pre-declared.

---

**Stop here. No `git add` / `git commit` has run. Awaiting operator / ChatGPT Gate 2 approval.**
