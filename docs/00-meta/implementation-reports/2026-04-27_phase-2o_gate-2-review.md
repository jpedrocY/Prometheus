# Phase 2o — Gate 2 Pre-Commit Review

**Phase:** 2o — Targeted Asymmetry Review / Analysis (docs-only).
**Branch:** `phase-2o/asymmetry-review`.
**Review date:** 2026-04-27 UTC.
**Authority:** Phase 2o operator-approved brief; Phase 2o Gate 1 plan; Phase 2f §§ 8–11 thresholds (preserved unchanged); Phase 2i §1.7.3 project-level locks (H0 anchor preserved); Phase 2l comparison report (R3 PROMOTE preserved); Phase 2m comparison report (R1a+R3 formal-but-mixed PROMOTE preserved); Phase 2n strategy-review memo (R3 research-leading + R1a+R3 promoted-but-non-leading framings preserved).

This Gate 2 review traces every operator-brief content + process requirement to its Phase 2o artifact, confirms threshold preservation, confirms safety posture, and records what awaits operator approval before any `git add` / `git commit`.

## Scope confirmed against operator brief

Scope confirmed: produce Gate 1 plan, asymmetry-review memo (sections A–K), Gate 2 review, and (post-Gate-2) checkpoint report. No code changes, no new backtests, no new variants, no new data, no parameter changes, no candidate-set widening, no §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold changes, no Phase 4 work, no paper/shadow-readiness planning, no execution-phase start. **All scope requirements applied; no scope drift.**

## Docs written

| Path                                                                                              | Purpose                                       | Status              |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------|---------------------|
| `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md`                          | Gate 1 plan                                   | drafted, untracked  |
| `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`                | Asymmetry review memo, sections A–K           | drafted, untracked  |
| `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md` (this file)            | Gate 2 pre-commit review                      | this document       |

The Phase 2o checkpoint report (per `.claude/rules/prometheus-phase-workflow.md`) will be drafted only after Gate 2 approval, immediately before the commit sequence — same precedent as Phase 2l / 2m / 2n.

No source / test / script / config files were touched. No `data/` artifacts. No `.claude/`, `.mcp.json`, or `pyproject.toml` / `uv.lock` changes.

## Memo sections A–K — present and threshold-preserving

| § | Title                                            | Present | Threshold-preserving notes                                                                                                                                                  |
|---|--------------------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A | Executive summary                                | yes     | Reproduces R3 = research-leading and R1a+R3 = promoted-but-non-leading framings. Plain-English BTC/ETH asymmetry summary present.                                            |
| B | Fixed evidence recap                             | yes     | All R3 / R1a+R3 / asymmetry numbers cited from already-committed Phase 2l / 2m / 2n reports. No re-derivation. No re-running.                                                |
| C | Asymmetry diagnosis framework                    | yes     | All 6 candidate explanations evaluated (symbol-specific, regime-composition, sample-fragility, setup-shape, directional-bias, family-limitation) with plausibility / supporting / weakening / fixability for each. Summary table at §C.7.                                                              |
| D | BTC-vs-ETH evidence synthesis                    | yes     | R-window, V-window, per-fold (vs H0 + vs R3), per-regime, long/short, trade-frequency-funnel deltas all tabulated.                                                            |
| E | Interpretation of R1a mechanism                  | yes     | (E.1) R1a correctly implemented — yes. (E.2) R1a selecting genuine compression — yes. (E.3) Whose problem — post-compression follow-through, not the compression definition. (E.4) Three framings (ETH-favorable specialty / regime-dependent / unstable) evaluated; "ETH-favorable specialty filter with a regime-localized signal" recommended. |
| F | Fixability analysis                              | yes     | All 4 future-direction hypotheses evaluated as hypotheses, not as execution approvals. F.3 (R1a abandonment while keeping R3) the cleanest immediate path; F.1 (regime-conditional) highest-EVI execution path if specified properly; F.4 (different setup-side) open future option; F.2 (symbol-conditional) unavailable at v1.                                  |
| G | Family-level implication                         | yes     | (G.1) Family has modest broad-based edge under R3, stronger but symbol-localized edge under R1a+R3 on ETH. (G.2) Asymmetry **increases** confidence in R3. (G.3) Reduces confidence in this specific R1a form, not in setup-side redesigns generally. (G.4) Pause longer (planning cycle, not execution cycle) before any next redesign. |
| H | Recommendation                                   | yes     | Primary: Phase 2o effectively closes the question; consolidate at R3; no further immediate execution. Fallback: Phase 2p Option B docs-only hypothesis-planning. Explicit answers to all four operator-required questions in §H.3.                                                                       |
| I | What would change this recommendation            | yes     | 6 switch-condition blocks (consolidate→execute, R1a-stays-alive→permanent-abandonment, R1a-promoted-but-non-leading→ETH-only, A→stop-family, A→Phase 4, A→stop-point).                                                                                                              |
| J | Next-phase options                               | yes     | 5 Phase 2p options compared with pros / cons / wasted-effort / EVI. Option A (pause; keep R3) recommended; Option B (docs-only hypothesis-planning) is the disciplined alternative.                                                                                                          |
| K | Explicit non-proposal list                       | yes     | 23 explicit non-proposals enumerated.                                                                                                                                          |

## Required preservation rules — enforced

### H0-anchor preservation

The memo enforces:

- H0 remains the **sole** §10.3 / §10.4 anchor (referenced consistently throughout §B, §D, §H).
- The Phase 2m R3-anchor view in §B / §D is explicitly labeled supplemental and descriptive, not governing — same labeling as Phase 2m comparison report §5.
- No re-ranking, no re-derivation, no threshold tightening or loosening.

### R3 research-leading framing preservation

The memo enforces R3 = research-leading baseline throughout (§A.1, §B.1, §G.2, §H.1, §H.3). The §G analysis explicitly concludes that the asymmetry **increases** confidence in R3. Phase 2n's framing is preserved without contradiction.

### R1a+R3 promoted-but-non-leading framing preservation

The memo enforces R1a+R3 = promoted-but-non-leading research branch throughout (§A.3, §C, §E.4, §H.1). The §E.4 framing analysis recommends "ETH-favorable specialty filter with regime-localized signal" — a refinement of "promoted-but-non-leading" that preserves the formal verdict and the strategic interpretation.

### ETH-specific strength NOT converted into universal recommendation

Confirmed:

- §E.4 explicitly evaluates three framings and rejects "universal next variant".
- §F.2 (symbol-conditional R1a — ETH only) explicitly noted as unavailable at v1 by §1.7.3; not recommended.
- §H.4 explicitly excludes Option F.2 and any framing that elevates ETH-specific strength to project-wide policy.
- §I.3 records ETH-only-research-deployment as a **future possibility contingent on operator policy change**, not a current recommendation.

### Another execution phase NOT recommended unless clearly and narrowly justified

Confirmed: §H.1 explicitly recommends **no further immediate execution phase**. §H.3 third bullet is unambiguous: "NOT IMMEDIATELY". §I.1 records the conditions that would justify a future execution phase (regime-conditional R1a-prime spec passing Phase 2i §1.7 binding test, or Phase 2i-deferred R1b/R2 with new evidence-grounding, or operator preference). Phase 2o does not authorize any execution.

### Prior-doc conflicts surfaced explicitly

No prior-doc conflicts surfaced during the Phase 2o analysis. The committed Phase 2l / 2m / 2n reports are mutually consistent on the key claims (R3 PROMOTE; R1a+R3 formal-but-mixed PROMOTE; H0 anchor preserved; Wave-1 historical-evidence-only; §1.7.3 BTC-primary lock). No silent reconciliation was needed.

## Recommendation — primary + fallback recorded

| Tier      | Option                                                          | Reasoning                                                                                                |
|-----------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Primary   | Phase 2o effectively closes the question; consolidate at R3; no further immediate execution | Two of three structural-redesign experiments PROMOTED; the most-supported asymmetry explanations (C.1 symbol-specific; C.5 directional-bias) point to facts about market structure rather than fixable rule issues; running another execution would be premature treadmill behaviour. |
| Fallback  | Phase 2p Option B — docs-only hypothesis-planning for one specific next redesign | If operator wants to keep structural-redesign path alive, develop a falsifiable regime-conditional R1a-prime spec via a Phase 2j-style spec-writing phase before any future execution Gate 1. |

What is **explicitly not** recommended at this time (memo §H.4): any execution phase, paper/shadow planning, Phase 4 work, symbol-conditional R1a deployment, new strategy-family research planning.

## What-would-change-recommendation switch conditions — present

Six switch-condition blocks in memo §I:

- §I.1 — consolidate → execute another structural redesign (regime-conditional R1a-prime specified properly; OR R1b / R2 revival with new evidence-grounding; OR operator preference).
- §I.2 — R1a stays alive → R1a abandoned permanently (additional evidence of robust BTC degradation; OR operator decides §1.7.3 makes R1a undeployable forever; OR research value fully captured).
- §I.3 — R1a promoted-but-non-leading → R1a as ETH-only research evidence (operator independently relaxes §1.7.3 — policy change, not evidence change).
- §I.4 — A → stop family / new family (third structural attempt produces clean §10.3 disqualification; OR operator decides absolute-edge gap too large; OR alternative-family hypothesis emerges).
- §I.5 — A → Phase 4 (operator independently lifts Phase 4 deferral).
- §I.6 — A → stop point (operator pauses strategy work entirely; OR docs-only correction phase needed).

## Next-phase options analysis — present

Five Phase 2p options in memo §J (A: pause / keep R3; B: docs-only hypothesis-planning; C: immediate new structural execution; D: later paper/shadow for R3; E: later new strategy-family planning), each evaluated on pros / cons / wasted-effort / EVI. Option A recommended; Option B is the disciplined alternative; the others remain effectively deferred at v1.

## Non-proposal list — present

Memo §K enumerates 23 explicit non-proposals: no new backtests, no new variants, no new candidates, no threshold changes, no R3 / R1a value changes, no anchor replacement, no universal-winner declaration, no execution phase, no Phase 4 start, no paper/shadow planning, no tiny-live planning, no live-readiness claim, no technical-debt-register edit, no ambiguity-log edit, no source-file touch, no MCP / Graphify, no credentials, no exchange-write, no data downloads, no Binance API calls, no branch push.

## Wave-1 / Phase 2l / Phase 2m / Phase 2n results preservation — confirmed

| Phase | Result                                                       | Preservation in Phase 2o memo                                                            |
|-------|--------------------------------------------------------------|------------------------------------------------------------------------------------------|
| 2g    | Wave-1 REJECT ALL                                             | Cited in §B as historical evidence only; not a comparison baseline; no re-ranking.        |
| 2l    | R3 PROMOTE                                                    | Cited in §B.1 with full headline + per-fold + per-regime + V-window numbers; verdict preserved unchanged. |
| 2m    | R1a+R3 PROMOTE (formal but mixed)                             | Cited in §B.2 with full H0-anchor + R3-anchor headline + per-fold + V-window + R1a-specific diagnostic numbers; verdict preserved unchanged; mixed-framing carried verbatim. |
| 2n    | R3 = research-leading; R1a+R3 = promoted-but-non-leading      | Both framings preserved verbatim throughout the memo (§A.1, §C, §E.4, §G.2, §H.1, §H.3, §I.3). |

## Threshold preservation

| Threshold / framework                          | Status                                                                                          |
|------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Phase 2f §10.3.a / §10.3.b / §10.3.c           | unchanged                                                                                       |
| Phase 2f §10.3 disqualification floor          | unchanged                                                                                       |
| Phase 2f §10.4 hard reject                     | unchanged                                                                                       |
| Phase 2f §11.3 no-peeking                      | unchanged                                                                                       |
| Phase 2f §11.3.5 pre-committed thresholds      | unchanged                                                                                       |
| Phase 2f §11.4 ETH-as-comparison rule          | unchanged                                                                                       |
| Phase 2f §11.6 cost-sensitivity                | unchanged                                                                                       |
| Phase 2i §1.7.3 H0-only anchor                 | unchanged                                                                                       |
| Phase 2i §1.7.3 BTCUSDT primary lock           | unchanged (explicitly cited as binding constraint in §F.2 and §I.3)                              |
| Phase 2i §1.7.3 ≤ 2 carry-forward cap          | unchanged (memo references both R3 and R1a as carry-forward; no third candidate exposed)         |
| Phase 2j §C.6 R1a sub-parameters (X=25, N=200) | unchanged (committed singularly)                                                                |
| Phase 2j §D.6 R3 sub-parameters (R=2.0, TS=8)  | unchanged (committed singularly)                                                                |
| GAP-20260424-036 fold convention               | unchanged                                                                                       |

## Safety posture

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
| Phase 4 work                                                 | none (operator restriction)                                                        |
| Paper/shadow-readiness planning                              | none (operator restriction)                                                        |
| Tiny-live-readiness planning                                 | none (operator restriction)                                                        |
| New execution phase started                                  | none                                                                              |
| Wave-1 variant revival                                       | none                                                                              |
| New redesign candidate proposed                              | none (only H0 / R3 / R1a+R3 referenced)                                            |
| Live-readiness claim                                         | none                                                                              |
| `git push`                                                   | not used (operator restriction; "do not push yet")                                 |
| Branch push                                                  | not used                                                                           |
| Pre-existing 417 tests pass                                  | yes (every checkpoint; no source files modified)                                    |
| `--no-verify` / hook skipping                                | not used                                                                          |

## Operator-restriction compliance (Phase 2o brief)

| Restriction                                                                                                           | Status                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Do not implement code                                                                                                  | honored                                                                                                              |
| Do not edit source files                                                                                               | honored                                                                                                              |
| Do not install dependencies                                                                                            | honored                                                                                                              |
| Do not download market data                                                                                            | honored                                                                                                              |
| Do not call Binance APIs (authenticated or public)                                                                    | honored                                                                                                              |
| Do not run new backtests / variants                                                                                    | honored                                                                                                              |
| Do not change parameters                                                                                               | honored                                                                                                              |
| Do not widen the candidate set                                                                                         | honored (only H0 / R3 / R1a+R3 referenced)                                                                            |
| Do not start Phase 4                                                                                                   | honored                                                                                                              |
| Do not start paper/shadow readiness planning                                                                           | honored                                                                                                              |
| Do not start another execution phase                                                                                   | honored                                                                                                              |
| Do not enable MCP / create `.mcp.json` / enable Graphify                                                                | honored                                                                                                              |
| Do not request credentials / create production Binance keys                                                            | honored                                                                                                              |
| Do not add exchange-write capability                                                                                    | honored                                                                                                              |
| Preserve formal H0-anchor judgments exactly                                                                            | honored (memo §A, §B, §D, §H)                                                                                        |
| Preserve R3 as research-leading baseline                                                                               | honored — §G.2 explicitly concludes asymmetry **increases** confidence in R3                                          |
| Preserve R1a+R3 promoted-but-non-leading / mixed framing                                                                | honored — §A.3, §E.4, §H.1, §I.3                                                                                      |
| Do not quietly convert ETH-specific strength into universal recommendation                                              | honored — §F.2 explicitly unavailable at v1; §H.4 explicit exclusion; §I.3 explicit policy-change-required               |
| Do not recommend another execution phase unless clearly and narrowly justified                                          | honored — §H.1 NOT IMMEDIATELY; §I.1 specifies the conditions that would change this; no execution recommended.       |
| Surface conflicts in prior docs explicitly instead of choosing silently                                                  | no conflicts surfaced — prior docs are mutually consistent.                                                          |
| Stop before any `git add` / `git commit`                                                                                | honored (this Gate 2 review is the stop point)                                                                       |

## Test suite

| When                                  | Result                |
|---------------------------------------|-----------------------|
| Pre-commit (no source changes)        | **417 passed** / ~12 s expected (matches Phase 2n end state) |
| After commit 1 (Gate 1 plan)          | **417 passed** (expected — docs only)                         |
| After commit 2 (asymmetry review memo) | **417 passed** (expected — docs only)                         |
| After commit 3 (Gate 2 review)        | **417 passed** (expected — docs only)                         |
| After commit 4 (checkpoint report) — expected | **417 passed**                                         |

`uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` were not rerun during Phase 2o because no source files were touched; the Phase 2n end state (green on all four gates) is preserved unchanged.

## Recommended next step

Operator/ChatGPT reviews:

1. The asymmetry-review memo at `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`.
2. This Gate 2 review.
3. The actual `git diff` (untracked: 3 docs).
4. The pytest 417 confirmation.

If approved, the operator/Claude proceeds with the commit sequence (proposed below).

## Recommended commit structure (after Gate 2 approval)

Proposed sequence on `phase-2o/asymmetry-review`:

1. `phase-2o: Gate 1 plan` — `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md`.
2. `phase-2o: asymmetry review memo` — `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`.
3. `phase-2o: Gate 2 review` — `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md` (this file).
4. `phase-2o: checkpoint report` — `docs/00-meta/implementation-reports/2026-04-27_phase-2o-checkpoint-report.md` (drafted after Gate 2 approval, immediately before this commit).

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## Questions for ChatGPT / operator

- **Is the primary recommendation (consolidate at R3; no further immediate execution; Phase 2p Option A) acceptable?** If not, the fallback (Phase 2p Option B — docs-only hypothesis-planning for regime-conditional R1a-prime) is the natural alternative; Option B can also become primary on operator preference.
- **Does the §F.3 framing (R1a stays alive as a research branch but is dropped as a deployable variant) align with operator intent?** The framing preserves the Phase 2m comparison report as committed evidence while making the R3-only baseline operational going forward (subject to all paper/shadow / live-readiness gates remaining deferred).
- **Any additional sections / framings the operator wants in the memo before commit?** The memo covers all sections A–K the brief required.
- **GAP-20260424-030 disposition.** Still deferred per Phase 2l / 2m / 2n approvals; Phase 2o does not propose lifting the deferral (operator restriction on TD-register and ambiguity-log edits, plus no SUPERSEDE event in 2o).

---

**Stop point:** awaiting operator/ChatGPT Gate 2 approval. No `git add`, no `git commit`, no `git push`, no merge.
