# Phase 2n — Checkpoint Report

Generated at the close of Phase 2n on branch `phase-2n/operator-strategy-review`, after Gate 2 approval. Four operator-authorized commits per the operator-approved commit sequence (this checkpoint is the fourth commit). Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2n — Operator / Strategy Review (docs-only).** A judgement-and-planning phase that synthesized the evidence accumulated through Phase 2g (Wave-1 REJECT ALL), Phase 2l (R3 PROMOTE), and Phase 2m (R1a+R3 formal PROMOTE with strategically mixed BTC/ETH evidence) and produced a recommendation about the breakout family's research-leading baseline, the framing of R1a+R3, and the highest-EVI next research step. No code changes, no new backtests, no new variants, no parameter changes, no §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework changes, no Phase 4 work, no paper/shadow-readiness planning.

## Goal

(a) Read the Phase 2g / 2h / 2i / 2j / 2k / 2l / 2m committed reports and the supporting strategy / backtesting / risk specs. (b) Produce a Gate 1 plan recording the scope, content requirements, preservation rules, and proposed deliverables. (c) Produce a substantive strategy-review memo with sections A–J per the operator brief. (d) Produce a Gate 2 pre-commit review tracing every operator-brief content + process requirement to its Phase 2n artifact. (e) Stop before any commit awaiting operator/ChatGPT Gate 2 approval; on approval, commit per the proposed sequence and produce this checkpoint.

## Summary

Phase 2n delivered four committable documentation artifacts (~1,650 lines of new content) and zero code / test / data changes. Pytest stayed at **417 passed** throughout (unchanged from Phase 2m end state — no source files touched). Ruff / format / mypy were not rerun in 2n (no source change); the Phase 2m end state (green on all four gates) is preserved unchanged.

The strategy-review memo's A–J sections produced:

1. **Candidate hierarchy.** H0 = framework anchor (descriptive baseline only; never a candidate). R3 = **research-leading baseline** (broad-based PROMOTE; project's strongest result). R1a+R3 = **promoted but non-leading branch** (formal PROMOTE under unchanged framework with H0 anchor; strategically mixed — helps ETH materially, hurts BTC materially relative to locked R3). Wave-1 = historical evidence only (REJECT ALL; never a comparison baseline).
2. **Mixed-promote interpretation.** Why H0-anchor PROMOTE is valid (framework discipline; §11.3.5 binding rule). Why R3-anchor view still matters strategically (R3 is the locked exit baseline for any future redesign). Why Phase 2m is not a clean replacement (Δexp_R3 has opposite signs across BTC and ETH; V-window amplifies the asymmetry). How BTC/ETH asymmetry should affect decision-making under Phase 2i §1.7.3 BTC-primary lock. Evidence classification: regime-conditional edge YES (R3 alone modestly; R1a+R3 stronger on ETH low_vol); symbol-specific edge YES (R1a+R3 ETH first positive-netPct V-window) — but only at research level under §1.7.3, not at v1 live. Fragile-conditional edge also still present (absolute aggregate still negative).
3. **Family-level judgement.** Family is "alive but not validated". Two of three structural-redesign experiments PROMOTED; the family responds to structural work; absolute performance remains negative on R for both promoted candidates. Continued research justified cautiously, with clear stopping criteria (a third structural-redesign attempt producing a clean §10.3 disqualification, or operator-determined absolute-edge-gap call, would justify family abandonment). Phase 2h §11.1 stopping rule (clean negative required) is not yet met.
4. **Decision options A–E** evaluated on pros / cons / wasted-effort / EVI / justification thresholds.
5. **Primary recommendation (provisional, evidence-based):** Option A — keep R3 as the research-leading version and stop further immediate redesign execution. **Fallback:** Option B — targeted asymmetry-review / analysis phase. **Explicitly NOT recommended at this time:** Option C (later paper/shadow for R3), Option D (later paper/shadow for R1a+R3), Option E (stop family / new family), Phase 4 work, live-readiness planning.
6. **Switch conditions** in §H enumerate six scenarios that would change the recommendation (A→B, A→execution, A→C/D, A→E, A→Phase 4, A→stop).
7. **Phase 2o options A–E** compared. Phase 2o Option A (docs-only asymmetry review) recommended as the disciplined continuation under the Phase 2n primary recommendation; the others remain effectively unavailable at v1 unless an independent operator-policy change occurs.
8. **Non-proposal list** in §J enumerates 21 explicit non-proposals (no new backtests, no new variants, no threshold changes, no R3 / R1a value changes, no anchor replacement, no universal-winner declaration, no Phase 4 start, no paper/shadow planning, no live-readiness claim, no technical-debt-register edit, no source-file touch, etc.).

### Operator Gate 2 framings preserved

The operator's Gate 2 approval added these explicit framings to be preserved in the checkpoint and reporting:

- **Do not frame R1a+R3 as the new universal winner.** Honored throughout the memo: §C.4 deliberately rejects the "new primary candidate" framing as incompatible with the BTC degradation evidence.
- **Do frame R3 as the research-leading baseline.** Honored: §C.2 records R3's broad-based PROMOTE evidence (R-window §10.3.a + §10.3.c on both symbols; first-ever positive BTC fold expR; all 6 regime cells improve; V-window confirms direction-of-improvement; clean implementation; robust to slippage and stop-trigger sensitivity) and §G.1 commits R3 as the baseline-of-record for any future structural-redesign work or operational-readiness planning.
- **Do frame R1a+R3 as a promoted but strategically mixed / non-leading branch.** Honored: §A.3 + §C.3 + §C.4 + §G.1 use this framing throughout. The mixed-promote framing the operator's Phase 2m Gate 2 approval committed ("promoted but strategically mixed candidate that requires a review phase before further execution or any deployment-readiness planning") is reproduced verbatim.
- **No further immediate execution phase is justified yet.** Honored: §G.1 explicitly recommends not starting Phase 2o execution unless a specific high-EVI hypothesis is independently developed.
- **No paper/shadow or Phase 4 work should begin yet.** Honored: §G.3 explicitly excludes both Options C / D and Phase 4 from current recommendation; §I lists them as deferred-future possibilities only; §H switch conditions specify what would change that.

## Files changed

By commit, on branch `phase-2n/operator-strategy-review` starting from `main @ a742309` (Phase 2m merge):

| Commit | Files                                                                                                              | +Lines |
|--------|--------------------------------------------------------------------------------------------------------------------|-------:|
| 1      | `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-1-plan.md` (new)                                     |  ~370  |
| 2      | `docs/00-meta/implementation-reports/2026-04-27_phase-2n_strategy-review-memo.md` (new)                            |  ~720  |
| 3      | `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-2-review.md` (new)                                   |  ~290  |
| 4      | `docs/00-meta/implementation-reports/2026-04-27_phase-2n-checkpoint-report.md` (new — this file)                   | this file |

## Files created

- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_strategy-review-memo.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n-checkpoint-report.md` (this file)

## Files deleted

None.

## Commands run

- `git -C c:/Prometheus status --short`, `git -C c:/Prometheus rev-parse --abbrev-ref HEAD`, `git -C c:/Prometheus log --oneline -5` — verified clean main with Phase 2m merged at `a742309`.
- `git -C c:/Prometheus checkout -b phase-2n/operator-strategy-review` — branch created from clean main.
- `git -C c:/Prometheus status --short`, `git -C c:/Prometheus diff --stat HEAD` at the evidence stop and at multiple checkpoints.
- `uv run pytest` at the evidence stop (417 passed / 12.17 s) and after each commit (expected 417 passed).
- `git add <specific-file>` + `git commit -m "<heredoc>"` four times per the operator-approved sequence (this checkpoint is the fourth commit).

No backtest runs. No data downloads. No `uv add` / `uv sync`. No `uv run ruff` / `uv run ruff format` / `uv run mypy` reruns (no source files modified; the Phase 2m end-state green status on those gates is preserved unchanged).

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None. No `configs/`, `.env`, `.claude/`, `.gitignore`, or `.gitattributes` edits.

## Tests/checks passed

| When                                  | Result                |
|---------------------------------------|-----------------------|
| Pre-commit (no source changes)        | **417 passed** / 12.17 s (matches Phase 2m end state) |
| After commit 1 (Gate 1 plan)          | **417 passed**         |
| After commit 2 (strategy review memo) | **417 passed**         |
| After commit 3 (Gate 2 review)        | **417 passed**         |
| After commit 4 (this) — expected      | **417 passed**         |

`uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` were not rerun during Phase 2n because no source files were touched; the Phase 2m end state (green on all four gates) is preserved unchanged.

## Tests/checks failed

None.

## Runtime output

Not applicable — Phase 2n produced no runtime state, no backtests, no scripts invoked.

## Known gaps

**No new GAP entries logged in this phase.** Phase 2n carries forward existing GAPs unchanged:

- GAP-20260420-028 OPEN-LOW (v002 manifest predecessor_version metadata) — unchanged.
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION (Phase 2e endpoint deferrals) — unchanged.
- GAP-20260420-029 RESOLVED (Phase 2e fundingRate Option C) — unchanged.
- GAP-20260424-030 OPEN — disposition deferred per Phase 2l / 2m Gate 2 approvals; Phase 2n does not create a SUPERSEDE event (no exit-philosophy change in 2n). Disposition stays deferred per operator brief: "do not edit technical-debt-register.md".
- GAP-20260424-031 / 032 / 033 OPEN — CARRIED. Phase 2n does not run any new sensitivity report cuts.
- GAP-20260424-034 / 035 RESOLVED verification-only.
- GAP-20260424-036 RESOLVED-by-convention (fold scheme; Phase 2h).

The strategy-review memo did not surface any prior-doc conflict that would require a permanent GAP entry. The committed Phase 2g / 2h / 2i / 2j / 2k / 2l / 2m reports are mutually consistent on the key claims (H0 as framework anchor; Wave-1 REJECT ALL preserved as historical evidence; R3 PROMOTE; R1a+R3 formal PROMOTE with strategically-mixed framing). No silent reconciliation was needed.

## Spec ambiguities found

None new. The Phase 2j memo §C R1a spec and §D R3 spec were sufficient for the strategy-level interpretation produced in Phase 2n. The §10.3 / §10.4 / §11.3.5 framework discipline produced unambiguous formal verdicts on both Phase 2l (R3 PROMOTE on §10.3.a + §10.3.c) and Phase 2m (R1a+R3 PROMOTE on §10.3.c BTC + §10.3.a + §10.3.c ETH). The strategic interpretation of the mixed Phase 2m verdict is judgement, not ambiguity — and the operator's Phase 2m Gate 2 approval established the binding framing ("promoted but strategically mixed") that Phase 2n preserved.

## Technical-debt updates needed

None made in 2n (operator restriction). The Phase 2n strategy review is informational input for any future operator review of TD-016 (statistical live-performance thresholds): the accumulated R3 + R1a+R3 evidence base, the regime-decomposition signals (R1a+R3 ETH low_vol PF 1.353; R1a+R3 ETH shorts PF 1.906; first positive-netPct V-window), and the BTC/ETH asymmetry pattern all inform the eventual TD-016 threshold determination. The register itself stays untouched until the operator explicitly lifts the Phase 2f restriction.

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
| Strategy / risk / dataset / cost-model changes               | none (docs-only)                                                                  |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (no run output produced)                                                      |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                                        |
| `docs/00-meta/implementation-ambiguity-log.md` edits         | none (none surfaced; operator restriction held)                                    |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only)                                            |
| Phase 2g / 2l / 2m run dirs untouched                        | yes                                                                                 |
| Wave-1 REJECT ALL preserved                                  | yes (historical evidence only; no comparison-baseline shifting)                     |
| Phase 2l R3 PROMOTE preserved                                | yes (designated as research-leading baseline; sub-parameters R-target=2.0 / TS=8 unchanged) |
| Phase 2m R1a+R3 PROMOTE preserved                            | yes (formal verdict unchanged; sub-parameters X=25 / N=200 unchanged; mixed-framing carried verbatim) |
| Phase 2i §1.7.3 project-level locks                          | preserved (BTCUSDT primary, one-position, 0.25% risk, 2× leverage, mark-price stops, v002 datasets, H0-only anchor, ≤ 2 carry-forward) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged                                                                                       |
| H0 anchor preservation                                        | enforced (memo §C.1, §D.1, §G.4)                                                              |
| Strategically-mixed-promote framing for Phase 2m              | preserved verbatim from operator Gate 2 approval                                                |
| `--no-verify` / hook skipping                                 | not used                                                                                      |
| `git push`                                                    | not used (operator restriction; "do not push yet")                                              |
| Phase 4 work                                                  | none (operator restriction)                                                                    |
| Phase 2o execution start                                      | none (operator restriction; "do not start Phase 2o yet"; this phase proposes 2o, does not start it) |
| Phase 2o Option A (asymmetry review) start                    | none (operator restriction; recommended as next phase, not started)                            |
| Paper/shadow-readiness planning                               | none (operator restriction)                                                                    |
| Tiny-live-readiness planning                                  | none (operator restriction)                                                                    |
| Live-readiness claim                                          | none                                                                                          |
| New backtests / variants / data                               | none                                                                                          |
| New redesign candidate exposed                                | none (only H0 / R3 / R1a+R3 referenced)                                                       |
| Disguised parameter sweeps                                    | none                                                                                          |
| Wave-1 variant revival                                        | none                                                                                          |
| New strategy family started                                   | none                                                                                          |
| Pre-existing 417 tests pass                                   | yes (every commit)                                                                              |

## Current runtime capability

Research-only, unchanged from end of Phase 2m. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0, the Phase 2g wave-1 variants, Phase 2l R3, and Phase 2m R1a+R3. No capability was added or removed in 2n.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design. No exchange adapter present, no order-placement code path, no credentials available.

## Recommended next step (proposal only — operator decides)

Per Gate 2 approval and the strategy-review memo §G + §I:

- **Primary recommendation: Phase 2o — docs-only targeted asymmetry review / analysis phase** (the natural continuation under Phase 2n's primary recommendation of "R3 as research-leading; stop further immediate execution"). Phase 2o Option A would examine the R1a BTC/ETH asymmetry in depth using Phase 2m's already-committed run artifacts (per-trade walkthrough of BTC R1a F2 / F4; per-regime decomposition of BTC R1a entries that produce 0% V-window WR; hypothesis generation for whether a regime-conditional R1a-prime variant would salvage BTC). Could escalate to a future execution phase if the diagnostic surfaces an actionable hypothesis; could close out as docs-only if not.
- **Fallback recommendation: pause strategy work entirely** until the operator independently develops a high-EVI next-axis hypothesis or independently lifts one of the deferred restrictions (Phase 4, paper/shadow planning, new strategy family).
- **Phase 2o is NOT yet started** by the Phase 2n closure. The Phase 2n operator brief explicitly says "do not start Phase 2o yet"; the Gate 2 approval reaffirms this. Phase 2o is the recommended next phase, but its own start gate is a separate operator decision.

Per Gate 2 approval, the following are **NOT** the next step at this time:

- **Phase 4 (runtime / state / persistence)** — stays deferred per operator policy.
- **Paper/shadow / live-readiness planning** — stays deferred per operator policy.
- **Another execution phase** (Phase 2o execution variant or otherwise) — stays deferred ("do not start another execution phase").
- **Phase 2o itself** is not authorized to start by the Phase 2n closure.

## Question for ChatGPT / operator

None. Phase 2n is complete. All operator brief content requirements applied; all process requirements honored; pytest is at 417 throughout (no source files modified); no new GAP entries needed; the Gate 2 approval explicitly preserved the strategic framings (R3 = research-leading; R1a+R3 = promoted but strategically mixed / non-leading branch) which the memo records throughout. The branch `phase-2n/operator-strategy-review` is complete and not yet pushed per operator restriction. Awaiting the operator's next-boundary decision (Phase 2o start authorization, or other).
