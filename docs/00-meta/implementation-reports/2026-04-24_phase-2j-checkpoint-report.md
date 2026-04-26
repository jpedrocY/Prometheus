# Phase 2j — Checkpoint Report

Generated at the close of Phase 2j on branch `phase-2j/structural-redesign-memo`, after Gate 2 approval. Three operator-authorized commits + this checkpoint = four commits total. Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2j — Structural Redesign Memo Only.** A docs-only phase following the Phase 2i recommendation (carry-forward set R1a + R3, capped at ≤ 2 per Gate 1 condition 1). Wrote complete rule specs for R1a (Volatility-percentile setup) and R3 (Fixed-R exit with time stop), pinned committed sub-parameter values singularly, defined candidate-specific falsifiable hypotheses against unchanged Phase 2f thresholds, and prepared the project for a future operator-approved execution-planning phase. No code changes, no new backtests, no new variants, no data, no API calls, no Phase 4 / Phase 2k / fallback Wave 2 start.

## Goal

(a) Apply the Phase 2i §1.7 binding structural-vs-parametric test to write complete rule specs for R1a and R3. (b) Pin each sub-parameter to a single committed value with research-default justification. (c) Define a falsifiable hypothesis for each candidate against unchanged §10.3 / §10.4 thresholds. (d) Map GAP-030/031/032/033 dispositions per candidate. (e) Restate the common validation framework with H0 as the only comparison anchor. (f) Issue an execution-readiness assessment (ready / needs-more-docs / drop) per candidate and a recommendation for which candidate(s) advance to a future Phase 2k. (g) Preserve the wave-1 verdict, the Phase 2h provisional recommendation, and the Phase 2i recommendation framing as inputs.

## Summary

Phase 2j delivered four committed artifacts across roughly 1,363 lines of inserted documentation and zero code / test / data changes:

1. Gate 1 plan (286 lines) — scope, non-goals, sub-parameter commitment policy, falsifiable-hypothesis structure, validation-framework restatement, GAP disposition map, anti-disguised-parameter-sweep discipline, preservation contracts, full safety checklist. Pre-approved by the operator's "Approved to start Phase 2j" message; committed alongside the other Phase 2j docs.

2. Structural redesign memo (600 lines) — 10-section memo (A executive summary; B fixed evidence recap; C full R1a spec with 16 sub-items; D full R3 spec with 18 sub-items; E side-by-side comparison; F common validation framework restated; G execution-readiness assessment; H provisional recommendation; I "what would change this recommendation"; J explicit non-proposal list).
   - **R1a — Volatility-percentile setup:** replaces H0's range-based + drift-cap setup-validity predicate with a percentile predicate (setup valid iff `atr_prior_15m ≤ 25th percentile of trailing-200-bar 15m ATR distribution`). Setup window stays at 8 bars strictly before the breakout candidate. Trigger / bias / entry / stop / exit / sizing all preserved from H0. Committed sub-parameters: X=25, N=200, warmup floor 221 bars. CARRIES GAP-030/031/032/033; supersedes nothing. Mandatory R1a-specific diagnostics: setup-validity rate per fold; ATR-percentile distribution at trade entries.
   - **R3 — Fixed-R exit with time stop:** replaces H0's seven-stage staged-trailing exit machinery with two terminal rules (take-profit at +2.0R; unconditional time-stop at 8 bars). Initial structural stop preserved exactly (never moved intra-trade). Setup / bias / trigger / entry / sizing preserved. Committed sub-parameters: R_TARGET=2.0, TIME_STOP_BARS=8 (anchored to existing project conventions). Same-bar priority: protective stop wins over take-profit. SUPERSEDES GAP-030 (break-even removed); CARRIES GAP-031/032; CARRIES-AND-EXTENDS GAP-033 (R3's time-stop is unconditional vs. H0's MFE-gated stagnation). New ExitReason values: TAKE_PROFIT, TIME_STOP. Mandatory R3-specific diagnostics: extended exit-reason histogram; R-multiple histogram of TAKE_PROFIT exits; time-stop bias diagnostic.
   - **Side-by-side comparison** ranks R3 first for execution: smaller implementation surface, lower fitting risk, sub-parameters anchored to existing project conventions, sharper falsifiability (§10.3.c strict-dominance applies). Both are READY for a future operator-approved execution-planning phase.
   - **Recommendation (provisional):** both R1a and R3 advance to Phase 2k, with R3 prioritized for first execution. Five switch-condition blocks in §I (only R1a; only R3; neither without more docs; fallback Wave 2 with H-D6; Phase 4). §J explicit non-proposal list reaffirms threshold preservation, wave-1 verdict preservation, no live deployment, no code, no MCP/Graphify, no TD-register edits.

3. Gate 2 review (319 lines) — Gate 1 ↔ memo traceability table for each operator process requirement; R1a and R3 spec completeness checks (16 / 18 items); side-by-side comparison check; common validation framework check; execution-readiness assessment check; recommendation check (provisional + 4 operator-choice paths); "What would change this recommendation" check (5 switch-condition blocks); explicit non-proposal list check (18 items); wave-1 result preservation; Phase 2h + Phase 2i recommendation preservation; threshold preservation table; §1.7.3 project-level locks preservation; disguised-parameter-sweep avoidance check; H0-only-anchor check; hidden-DOF callout check; prior-doc conflict check (none); full safety posture; operator restrictions compliance.

4. This checkpoint report.

No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `.mcp.json`, `data/`, or `technical-debt-register.md` edits. No ambiguity-log changes (no new GAP needed; the §1.7 binding test plus existing thresholds plus per-candidate spec disciplines handled every judgement). Pytest stayed at **396 passed** throughout (same count as end of Phase 2i — zero code changes).

## Files changed

By commit, on branch `phase-2j/structural-redesign-memo` starting from `main @ 8a34f20` (Phase 2i merge):

| Commit | SHA       | Files                                                                                                              | +Lines |
|--------|-----------|--------------------------------------------------------------------------------------------------------------------|-------:|
| 1      | `b5f0b74` | `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md` (new)                                     |  +286  |
| 2      | `b7283cd` | `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md` (new)                        |  +600  |
| 3      | `5bf2e7a` | `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md` (new)                                   |  +319  |
| 4      | (this)    | `docs/00-meta/implementation-reports/2026-04-24_phase-2j-checkpoint-report.md` (new)                               | this file |

## Files created

- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j-checkpoint-report.md` (this file)

## Files deleted

None.

## Commands run

- `git checkout -b phase-2j/structural-redesign-memo` (once at phase start, from clean `main`).
- `git status --short`, `git diff --stat`, `git log --oneline -*` at multiple checkpoints.
- `uv run pytest` before each commit and at the evidence stop (five runs across the phase) — every run `396 passed` in ~11–12 seconds.
- `git add <specific-file>` + `git commit -m "<heredoc>"` three times for commits 1–3. Commit 4 (this checkpoint) follows immediately.

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None. No `configs/`, `.env`, `.claude/`, `.gitignore`, or `.gitattributes` edits.

## Tests/checks passed

| When                                  | Result                |
|---------------------------------------|-----------------------|
| Pre-commit-1                          |  396 passed / 12.46s  |
| After commit 1 (Gate 1 plan)          |  396 passed / 12.37s  |
| After commit 2 (redesign memo)        |  396 passed / 11.85s  |
| After commit 3 (Gate 2 review)        |  396 passed / 12.18s  |
| After commit 4 (this) — expected      |  396 passed           |

`uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` were not rerun during Phase 2j because no source files were touched; the Phase 2i end-state (green on all four gates) is preserved unchanged.

## Tests/checks failed

None.

## Runtime output

Not applicable — Phase 2j produced no runtime state, no backtests, no scripts invoked.

## Known gaps

**No new GAP entries logged in this phase.** The Phase 2i §1.7 structural-vs-parametric binding test, the Phase 2f §9.1 / §10.3 / §10.4 / §11.3 thresholds, and the per-candidate spec disciplines (R1a's tie-breaking convention; R3's same-bar priority and unconditional-time-stop interpretation) handled every structural-vs-parametric judgement made in the redesign memo. No new ambiguity surfaced that required a permanent ambiguity-log entry.

Prior GAPs unchanged. Pre-existing dispositions:

- GAP-20260420-028 OPEN-LOW (v002 manifest predecessor_version metadata).
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION (Phase 2e endpoint deferrals).
- GAP-20260420-029 RESOLVED (Phase 2e fundingRate Option C).
- GAP-20260424-030 OPEN — **flagged for SUPERSEDED-on-execution** when R3 advances per Phase 2j memo §D.16.
- GAP-20260424-031 OPEN — CARRIED by both R1a and R3 (no candidate touches the bias rule).
- GAP-20260424-032 OPEN — CARRIED by both R1a and R3 as a mandatory mark-price-sensitivity report cut for any future execution wave.
- GAP-20260424-033 OPEN — **flagged for CARRIED-AND-EXTENDED-on-execution** when R3 advances per Phase 2j memo §D.16 (R3's unconditional time-stop interpretation).
- GAP-20260424-034 / 035 RESOLVED verification-only (Phase 2f).
- GAP-20260424-036 RESOLVED-by-convention (fold scheme; Phase 2h).

The "flagged for SUPERSEDED-on-execution" status is recorded inline in the redesign memo §D.16 and §C.14; the actual ambiguity-log SUPERSEDED status update will happen in the future Phase 2k execution phase when R3 begins (or stays CARRIED if R3 is dropped).

## Spec ambiguities found

None new in 2j. R1a's percentile-rank tie-breaking (stable order) and R3's same-bar STOP-vs-TAKE_PROFIT priority (stop wins) are spec-internal choices made within the memo's spec sections, not GAPs against the v1 spec or any prior-phase doc. The §1.7 binding test and the per-candidate spec writing handled every decision without requiring a new ambiguity-log entry.

## Technical-debt updates needed

None made in 2j (operator restriction). The redesign specs are informational input for any future operator review of TD-016 (statistical live-performance thresholds): if R1a or R3 produces evidence, that evidence informs TD-016's threshold determination. The register itself stays untouched until the operator explicitly lifts the Phase 2f restriction.

## Safety constraints verified

| Check                                                        | Result |
|--------------------------------------------------------------|--------|
| Production Binance keys                                      | none   |
| Exchange-write code                                          | none   |
| REST / WebSocket / authenticated endpoints                   | none   |
| Credentials / `.env`                                         | none   |
| `.mcp.json`                                                  | absent |
| Graphify                                                     | disabled |
| MCP servers                                                  | not activated |
| Manual trading controls                                      | none   |
| Strategy structural changes                                  | none in 2j (specs only) |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none   |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (Phase 2j produced no runtime / data output) |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction) |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only) |
| Phase 2g run dirs untouched                                  | yes |
| Wave-1 result preserved                                      | yes (REJECT ALL stands; no re-derivation) |
| Phase 2h provisional recommendation preserved                | yes (input, not target for revision) |
| Phase 2i recommendation preserved                            | yes (carry-forward R1a + R3, ≤ 2 cap, R1 split, H0 anchor) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged |
| §1.7.3 project-level locks                                   | preserved (Family-R risk redesigns excluded; one-position lock honored) |
| Pre-existing 396 tests pass                                  | yes (every commit) |
| `--no-verify` / hook skipping                                | not used |
| `git push`                                                   | not used (operator restriction) |
| Phase 4 work                                                 | none (operator restriction) |
| Phase 2k execution-planning work                             | none (operator restriction; this phase proposes 2k, does not start it) |
| Fallback Wave 2 / H-D6 start                                 | none (operator restriction) |
| Comparison of redesign candidates to wave-1 as baselines     | none (H0 only) |
| Disguised parameter sweeps                                   | none (single committed value per sub-parameter) |
| Carry-forward expansion beyond R1a + R3                      | none |

## Current runtime capability

Research-only, unchanged from end of Phase 2i. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0 or any approved variant; no capability was added or removed in 2j.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design.

## Forwarding notes for Phase 2k (per operator non-blocking note)

When Phase 2k is planned, the Gate 1 plan should explicitly restate the following items so they are not lost in transit:

- **R3 same-bar priority**: when a single 15m bar simultaneously satisfies the protective-stop hit condition AND the take-profit condition (price reaches `entry_price + R_TARGET × initial_R` in the same bar that the mark-price stops out), the **protective stop wins**. This is the conservative, H0-aligned choice and is recorded in the redesign memo §D.3.
- **The new exit-reason taxonomy for R3**: `ExitReason` extends with `TAKE_PROFIT` and `TIME_STOP` (the existing `STOP`, `TRAILING_BREACH`, `STAGNATION`, `END_OF_DATA` values are unchanged in code, but R3 will not emit `TRAILING_BREACH` or `STAGNATION` because the underlying logic is removed). The trade-record schema and the monthly/yearly aggregator both need extension. This is recorded in the redesign memo §D.10 and §D.18.
- **R3 is still judged under the same Phase 2f framework**: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds apply unchanged. **§10.3.c (exit-model bake-off strict dominance) is treated as an additional strict-dominance promotion path if applicable, not as a framework rewrite.** The primary promotion paths for R3 remain §10.3.a (Δexp ≥ +0.10R AND ΔPF ≥ +0.05) and §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse > 1.0pp); §10.3.c is available as a third path because R3 is structurally an exit-philosophy change. This is recorded in the redesign memo §D.17.

These three items are non-blocking for Phase 2j closure but should be reproduced verbatim in the Phase 2k Gate 1 plan when it is approved.

## Recommended next step (proposal only — operator decides)

The Phase 2j structural redesign memo §H records a **provisional** recommendation, not a binding decision. The operator chooses among the options the memo analyzes:

- **Phase 2k execution-planning, both R1a and R3 (provisional primary)** — both READY per §G.3; R3 prioritized for first execution per §E.
- **Phase 2k execution-planning, R1a only** (operator switch condition §I.1).
- **Phase 2k execution-planning, R3 only** (operator switch condition §I.2).
- **Neither advance; another docs phase** (operator switch condition §I.3).
- **Fallback Wave 2 with H-D6** (operator switch condition §I.4).
- **Phase 4** (operator switch condition §I.5; requires explicit policy change).

The §I switch-condition blocks make the conditions for changing the recommendation explicit and pre-declared, the same way Phase 2f's §10.3 / §10.4 thresholds were pre-declared for wave 1.

## Question for ChatGPT / operator

None. Phase 2j is complete. All Gate 1 plan requirements applied; all operator process requirements honored; pytest is at 396 throughout. The operator's non-blocking note about Phase 2k forwarding items has been recorded above (§"Forwarding notes for Phase 2k"). Awaiting the operator's next-boundary decision among Phase 2k Options / fallback Wave 2 / Phase 4.
