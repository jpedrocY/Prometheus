# Phase 2i — Checkpoint Report

Generated at the close of Phase 2i on branch `phase-2i/structural-redesign-planning`, after Gate 2 approval. Three operator-authorized commits + this checkpoint = four commits total. Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2i — Structural Breakout Redesign Planning.** A decision/planning-only phase following the Phase 2h provisional Option B recommendation. Defines structural-vs-parametric for the v1 breakout family, evaluates five redesign axes, runs the R1 coherence test required by Gate 1 condition 2, proposes a candidate shortlist where each candidate is a genuine rule-shape change, surfaces GAP-030/031/032/033 interactions per candidate, and recommends a carry-forward set capped at ≤ 2 per Gate 1 condition 1 with the explicit H0-anchor statement per Gate 1 condition 3. No code changes, no new backtests, no new variants, no data, no API calls, no Phase 4 work, no fallback-Wave-2 start.

## Goal

(a) Recap the locked facts from Phase 2e baseline / Phase 2f review / Phase 2g wave-1 / Phase 2h decision memo. (b) Produce a binding structural-vs-parametric test that prevents Phase 2j from quietly relabeling parameter tweaks as "structural". (c) Evaluate five redesign axes (S setup-pattern, B HTF bias/regime, E entry-timing, X exit-philosophy, R risk/position-management interaction). (d) Run the R1 coherence test and either keep R1 as one bundled candidate or split it into R1a + R1b. (e) Propose a candidate shortlist; recommend a carry-forward set capped at ≤ 2 candidates. (f) Surface per-candidate GAP-030/031/032/033 dispositions. (g) Define the redesign validation framework with H0 as the only comparison anchor. (h) Compare four next-phase options and recommend the highest-value path forward.

## Summary

Phase 2i delivered four committed artifacts across roughly 1,532 lines of inserted documentation and zero code / test / data changes:

1. Gate 1 plan (647 lines) — scope, non-goals, factual recap, structural-vs-parametric binding test, five-axis evaluation, candidate shortlist (pre-split frame R1/R2/R3 + post-split-frame pointer), GAP interaction matrix, validation framework, four-option analysis for Phase 2j, provisional recommendation with explicit "what would change this recommendation" switch conditions, full safety checklist. All three operator Gate 1 conditions applied inline (§26). Gate 2 documentation consistency fix applied: stale "3 candidates max" / "R1/R2/R3" / "1–3 candidates" sections labeled as the pre-split initial frame with pointers to the post-split (up to 4 candidates) frame.

2. Structural redesign analysis memo (463 lines) — three clearly separated parts. Part 1 factual recap + binding structural-vs-parametric definition. Part 2 five-axis evaluation; **R1 coherence test concluded R1 is two separable ideas, not one coherent thesis** — split into R1a (Family-S setup-pattern volatility-percentile) and R1b (Family-B HTF bias/regime); 4-candidate shortlist (R1a, R1b, R2 pullback-confirmed entry, R3 fixed-R exit with time stop); 4-candidate × 4-GAP disposition matrix; validation framework with the explicit H0-anchor statement and mandatory diagnostics. Part 3 recommended carry-forward set **R1a + R3** (provisional, capped at ≤ 2 per Gate 1 condition 1) with reasoning and explicit non-inclusion rationale for R1b and R2; Phase 2j Option A (memo only) as primary, Option B (execution planning) as fallback; five switch-condition blocks; explicit non-proposal list.

3. Gate 2 review (264 lines) — Gate 1 ↔ memo traceability table, three Gate 1 conditions explicitly mapped to memo locations, structural-vs-parametric definition presence check, five-axis evaluation completeness check, R1 coherence test outcome verification, 4-candidate shortlist verification, GAP disposition matrix verification, validation framework verification (including H0-anchor statement), recommendation framing check (provisional + ≤ 2 carry-forward), wave-1 result + Phase 2h recommendation + threshold + project-level-lock preservation tables, full safety posture, no-new-GAP-needed declaration with reasoning.

4. This checkpoint report.

No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `.mcp.json`, `data/`, or `technical-debt-register.md` edits were made at any point. No ambiguity-log changes (no GAP-037; the §1.7 binding test plus existing Phase 2f thresholds plus the Gate 1 condition framework handled every structural-vs-parametric judgement). Pytest stayed at **396 passed** throughout (same count as end of Phase 2h — zero code changes).

## Files changed

By commit, on branch `phase-2i/structural-redesign-planning` starting from `main @ 61696a6` (Phase 2h merge):

| Commit | SHA       | Files                                                                                                          | +Lines |
|--------|-----------|----------------------------------------------------------------------------------------------------------------|-------:|
| 1      | `75f8069` | `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md` (new)                                 |  +647  |
| 2      | `782ea5d` | `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md` (new)                           |  +463  |
| 3      | `f026e62` | `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md` (new)                               |  +264  |
| 4      | (this)    | `docs/00-meta/implementation-reports/2026-04-24_phase-2i-checkpoint-report.md` (new)                           | this file |

## Files created

- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2i-checkpoint-report.md` (this file)

## Files deleted

None.

## Commands run

- `git checkout -b phase-2i/structural-redesign-planning` (once at phase start, from clean `main`).
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
| Pre-commit-1                          |  396 passed / 11.78s  |
| After commit 1 (Gate 1 plan)          |  396 passed / 11.49s  |
| After commit 2 (redesign-analysis)    |  396 passed / 11.62s  |
| After commit 3 (Gate 2 review)        |  396 passed / 11.54s  |
| After commit 4 (this) — expected      |  396 passed           |

`uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` were not rerun during Phase 2i because no source files were touched; the Phase 2h end-state (green on all four gates) is preserved unchanged.

## Tests/checks failed

None.

## Runtime output

Not applicable — Phase 2i produced no runtime state, no backtests, no scripts invoked against exchange or data sources.

## Known gaps

**No new GAP entries logged in this phase.** The §1.7 binding test (structural-vs-parametric definition), the Phase 2f §9.1 / §10.3 / §10.4 / §11.3 thresholds, and the Gate 1 condition framework handled every structural-vs-parametric judgement made in the redesign-analysis memo. No new ambiguity surfaced that required a permanent ambiguity-log entry. Phase 2i Gate 1 plan §19 anticipated this case ("if no new GAP is needed, the ambiguity log is unchanged").

Prior GAPs unchanged. In particular GAP-20260420-028 remains OPEN-LOW from Phase 2e; GAP-20260419-018 / 020 / 024 remain ACCEPTED_LIMITATION; GAP-20260420-029 RESOLVED; GAP-20260424-030 / 031 / 032 / 033 remain OPEN strategy items from Phase 2f; GAP-20260424-034 / 035 RESOLVED verification-only; GAP-20260424-036 (fold-scheme convention) RESOLVED-by-convention from Phase 2h.

## Spec ambiguities found

None new. The R1 coherence test was a *memo-level analytical conclusion* using the §1.7 binding test, not a spec ambiguity. The Family-R exclusion was an *enforcement* of §1.7.3 project-level locks, not a spec ambiguity. The R3 vs. H-D6 distinction was *clarified* via Phase 2f §9.1 single-axis-vs-parametric, not a spec ambiguity.

## Technical-debt updates needed

None made in 2i (operator restriction). The wave-1 result (REJECT ALL), the Phase 2h provisional recommendation, and the Phase 2i recommendation are informational input for any future operator review of TD-016 (statistical live-performance thresholds). The register itself stays untouched until the operator explicitly lifts the Phase 2f restriction.

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
| Strategy structural changes                                  | none in 2i (proposal only) |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none   |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (Phase 2i produced no runtime / data output) |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction) |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only) |
| Phase 2g run dirs untouched                                  | yes |
| Wave-1 result preserved                                      | yes (REJECT ALL stands; no re-derivation) |
| Phase 2h provisional recommendation preserved                | yes (input, not target for revision) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged |
| §1.7.3 project-level locks                                   | preserved (Family-R risk redesigns excluded; one-position lock honored) |
| Pre-existing 396 tests pass                                  | yes (every commit) |
| `--no-verify` / hook skipping                                | not used |
| `git push`                                                   | not used (operator restriction) |
| Phase 4 work                                                 | none (operator restriction) |
| Phase 2j work                                                | none (operator restriction; this phase proposes 2j, does not start it) |
| Fallback Wave 2 start                                        | none (operator restriction) |

## Current runtime capability

Research-only, unchanged from end of Phase 2h. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0 or any approved variant; no capability was added or removed in 2i.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design.

## Recommended next step (proposal only — operator decides)

The Phase 2i decision-analysis memo §3.3 and §3.4 record a **provisional** recommendation, not a binding decision. The operator chooses among the four options the memo analyzes:

- **Phase 2j Option A (provisional primary)** — Structural redesign memo only (docs-only) with carry-forward set **R1a + R3** (or operator-modified pair within the ≤ 2 cap from the post-split shortlist R1a/R1b/R2/R3).
- **Phase 2j Option B (provisional fallback)** — Redesign candidate execution planning. Applicable only if Phase 2j Option A's spec writing narrows to a single fully-specified candidate.
- **Phase 2j Option C** — Fallback narrow Wave 2 with H-D6 (memo §3.4 "switch from A → C").
- **Phase 2j Option D** — Phase 4 (memo §3.4 "switch from A → D"; requires explicit operator policy change).

The decision-analysis memo §3.4 enumerates five switch-condition blocks (change carry-forward set; A → B; A → C; A → D; A → defer) so the operator's choice can be measured against pre-declared evidence/reasoning conditions, the same way Phase 2f's §10.3 / §10.4 thresholds were pre-declared for wave 1.

## Question for ChatGPT / operator

None. Phase 2i is complete. All three Gate 1 conditions and all Phase 2i operator restrictions were honored. Pytest is at 396 throughout. Awaiting the operator's next-boundary decision among Phase 2j Options A / B / C / D.
