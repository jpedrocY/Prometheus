# Phase 2n — Gate 1 Plan

**Phase:** 2n — Operator / Strategy Review.
**Branch:** `phase-2n/operator-strategy-review`.
**Plan date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

---

## 1. Purpose

Phase 2l produced the project's first PROMOTE verdict (R3 — fixed-R take-profit + unconditional time-stop). Phase 2m produced the second (R1a+R3 — volatility-percentile setup on top of R3's locked exit baseline) under the unchanged Phase 2f §10.3 framework with H0 as the sole anchor, **but with strategically mixed evidence**: R1a materially helps ETH (Δexp_R3 +0.237 R, ΔPF_R3 +0.359, V-window +0.69% netPct) and materially hurts BTC (Δexp_R3 −0.180 R, ΔPF_R3 −0.205, V-window 4 trades / 0% WR / expR −0.990).

Phase 2n is a **docs-only operator / strategy review phase**. It does not run new backtests, change source code, or change the Phase 2f framework. It synthesizes the evidence accumulated through Phase 2g / 2l / 2m, judges what the breakout family currently looks like, and recommends what the highest-value next research step is.

This is judgement and planning only. The Phase 2m operator-approved framing — "R1a+R3 is a promoted but strategically mixed candidate that requires a review phase before further execution or any deployment-readiness planning" — is the starting position; Phase 2n is that review phase.

## 2. Plain-English statement

The project has now run two structural-redesign experiments. R3 produced a clean broad-based improvement on both BTC and ETH. R1a (added on top of R3) helped ETH a lot and hurt BTC a bit. Both candidates formally PROMOTE under the unchanged framework against the H0 anchor, but they tell different strategic stories. Phase 2n is the operator's chance to step back, look at the family-wide picture, decide which candidate (R3 alone or R1a+R3) is the project's research-leading version, decide whether the family has earned more research investment, and decide what should happen next.

## 3. Branch and status verification commands

Already executed at phase start:

```
git -C c:/Prometheus status --short                     # clean
git -C c:/Prometheus rev-parse --abbrev-ref HEAD        # main
git -C c:/Prometheus log --oneline -5                   # 2m merged at a742309
git -C c:/Prometheus checkout -b phase-2n/operator-strategy-review
```

Working tree clean before this phase started. `main` is at `a742309` (Phase 2m merge); `origin/main` matches.

## 4. Exact scope

- Read the Phase 2g / 2h / 2i / 2j / 2k / 2l / 2m committed reports in full (already familiar from prior conversations; re-confirm against on-disk text where ambiguity arises).
- Read the supporting docs the operator brief cites (strategy spec, backtest plan, validation checklist, backtesting principles, walk-forward validation, cost modeling, position-sizing framework, stop-loss policy, exposure limits).
- Produce a written **strategy-review memo** with sections A–J per the operator brief.
- Produce a **Gate 2 pre-commit review** that traces every operator-brief content + process requirement to its Phase 2n artifact.
- Produce the **Phase 2n checkpoint report** (after Gate 2 approval, immediately before commits).
- Stop before any commit, awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

Per the operator brief:

- No code changes.
- No source-file edits (`src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `uv.lock`, `.claude/`, `.gitignore`, `.gitattributes`).
- No new tests.
- No new backtests, runs, or variants.
- No re-running of any existing variant (H0, R3, R1a+R3, or any wave-1 variant).
- No parameter changes.
- No widening of the candidate set.
- No new data downloads, no new dataset versions, no manifest changes.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work.
- No paper/shadow-readiness planning. No live-readiness planning.
- No execution-phase start (Phase 2o or otherwise).
- No edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- No `data/` commits.
- No re-derivation, re-ranking, or threshold-tightening / threshold-loosening of the §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework.
- No quiet replacement of H0 as the formal framework anchor.
- No quiet declaration of R1a+R3 as the new universal winner.
- No live deployment, paper/shadow readiness, or capital exposure proposal.

## 6. Factual recap to be reproduced in the memo

(All numbers quoted from already-committed reports; the memo cites each.)

### 6.1 Phase 2e baseline (FULL window 51 months; v002 datasets)

- BTC: 41 trades, WR 29.27%, expR −0.43, PF 0.32, net −3.95%, max DD −4.23%.
- ETH: 47 trades, WR 23.40%, expR −0.39, PF 0.42, net −4.07%, max DD −4.89%.
- Funnel dominant rejections: `no valid setup` ~57–58%, `neutral bias` ~37%, `no close-break` ~5%.
- Descriptive baseline only; not promotion evidence.

### 6.2 Phase 2g wave-1 result (committed)

REJECT ALL — H-A1 / H-B2 / H-C1 / H-D3 all disqualified on BTC under §10.3 disqualification floor, with H-B2 the closest case (vetoed by |maxDD| > 1.5× baseline ratio 1.505x). Wave-1 evidence is preserved as historical evidence only; no comparison-baseline shifting.

### 6.3 Phase 2l R3 result (committed)

R-window:
- H0 BTC 33 / 30.30% / −0.459 / 0.255 / −3.39% / −3.67%.
- R3 BTC 33 / 42.42% / **−0.240** / **0.560** / −1.77% / −2.16%.
- H0 ETH 33 / 21.21% / −0.475 / 0.321 / −3.53% / −4.13%.
- R3 ETH 33 / 33.33% / **−0.351** / **0.474** / −2.61% / −3.65%.

§10.3 verdict: PROMOTE on both BTC (§10.3.a + §10.3.c) and ETH (§10.3.a + §10.3.c). Per-fold: R3 beats H0 in 4/5 BTC folds and 3/5 ETH folds. Per-regime: R3 improves expR in **all 6** regime-symbol cells (after the operator-required corrected diagnostic). V-window confirms direction-of-improvement on both symbols.

### 6.4 Phase 2m R1a+R3 result (committed)

R-window:
- R1a+R3 BTC 22 / 27.27% / **−0.420** / **0.355** / −2.07% / −2.33%.
- R1a+R3 ETH 23 / 34.78% / **−0.114** / **0.833** / −0.59% / −2.96%.

H0-anchor §10.3 verdict: PROMOTE.
- BTC clears §10.3.c **only** (Δexp +0.039 below the §10.3.a +0.10 threshold; ΔPF +0.100; Δ|maxDD| −1.341 pp).
- ETH clears §10.3.a **and** §10.3.c (Δexp +0.362 R, ΔPF +0.512, Δ|maxDD| −1.171 pp).

R3-anchor (descriptive) deltas: BTC Δexp −0.180 / ΔPF −0.205; ETH Δexp +0.237 / ΔPF +0.359.

V-window:
- R1a+R3 ETH **first positive netPct ever**: 8 trades / 62.5% WR / expR +0.386 / PF 2.222 / netPct +0.69%.
- R1a+R3 BTC severely degraded: 4 trades / 0% WR / expR −0.990 / netPct −0.88%.

R1a-specific diagnostic: 100% of filled R1a entries at ATR percentile ≤ 25% (predicate working as designed).

### 6.5 What the project has proved technically

- The data layer (v002 manifests, 51-month coverage, mark-price + funding joins) is research-credible.
- The backtester is deterministic at fixed inputs and reproduces baselines bit-for-bit across phases.
- The variant-config + stop-trigger-source + setup-predicate-kind infrastructure works.
- Pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied without post-hoc adjustment have produced two PROMOTE verdicts (R3, R1a+R3) and one REJECT-ALL verdict (Wave-1).
- The framework discipline holds: H0 anchor preserved through Phase 2l + Phase 2m without quiet replacement; supplemental anchors clearly labeled as descriptive only.

### 6.6 What remains unresolved strategically

These are the questions Phase 2n must address:

1. **Is R3 alone now the research-leading baseline?** R3 promotes broadly on R and V; R1a+R3 promotes formally but with asymmetric BTC/ETH outcomes. Should subsequent phases treat R3 alone as the standard variant?
2. **What is the right framing for R1a+R3?** Universal winner? ETH specialty? Promoted but non-leading branch?
3. **Has the breakout family earned more research investment, or is the case for further structural-redesign work weakening?**
4. **What is the highest-value next step?** Continue this family's optimization, attempt one of the deferred candidates (R1b, R2), prepare for paper/shadow on R3 alone (deferred per operator policy), or shift to a new family?

Phase 2n produces a recommendation, not a decision. The operator decides.

## 7. What Phase 2n is NOT

- Phase 2n is **not** a re-judgement of the §10.3 / §10.4 framework. The framework's verdicts (REJECT ALL on Wave-1; PROMOTE on R3; PROMOTE on R1a+R3) stand as committed.
- Phase 2n is **not** a new ranking exercise that tries to re-pick which candidate "wins". The H0 anchor is preserved.
- Phase 2n is **not** a deployment recommendation. It does not propose paper/shadow, tiny-live, or any operational-readiness work in this phase.
- Phase 2n is **not** a code phase. No source files, no tests, no scripts touched.
- Phase 2n is **not** an attempt to reconcile a "true winner" — strategic interpretation is allowed to differ from formal ranking.

## 8. Memo content requirements (per operator brief)

The strategy-review memo will have sections A–J:

| § | Title                                          | Brief description                                                                                  |
|---|------------------------------------------------|----------------------------------------------------------------------------------------------------|
| A | Executive summary                              | What Phase 2n does, why review not execution, plain-English family-state summary                   |
| B | Fixed evidence recap                           | H0 / Wave-1 / R3 / R1a+R3 facts, technical-known vs strategically-unresolved                       |
| C | Candidate hierarchy analysis                   | H0 / R3 / R1a+R3 status; research-leading-baseline judgement; R1a+R3 framing decision              |
| D | Interpretation of the mixed Phase 2m result    | Why H0-anchor PROMOTE is valid; why R3-anchor still matters; BTC/ETH asymmetry analysis             |
| E | Family-level judgement                         | Has breakout family earned continued research? Is R3 enough? Does R1a strengthen the family?       |
| F | Decision options analysis (≥ 5 options)        | A–E options with pros/cons/wasted-effort/EVI/justification thresholds                              |
| G | Recommendation                                 | Primary + fallback with explicit reasoning                                                          |
| H | What would change this recommendation          | Switch conditions for each direction                                                                |
| I | Next-phase options (≥ 5 options)               | Phase 2o variants compared on pros/cons/wasted-effort/EVI                                          |
| J | Explicit non-proposal list                     | What Phase 2n explicitly does not do                                                                |

## 9. Required preservation rules

The memo must enforce:

1. **The formal H0-anchor judgments are preserved exactly as recorded.** R3 PROMOTES on R via §10.3.a + §10.3.c; R1a+R3 PROMOTES on R via §10.3.c (BTC) + §10.3.a + §10.3.c (ETH).
2. **The strategic interpretation that Phase 2m is a mixed / symbol-asymmetric promote is preserved verbatim.** The operator's Gate 2 framing — "promoted but strategically mixed candidate that requires a review phase before further execution or any deployment-readiness planning" — is reproduced.
3. **H0 is not quietly replaced as the formal framework anchor.** Any descriptive R3-anchor or R1a+R3-anchor analysis is explicitly labeled as supplemental.
4. **R1a+R3 is not quietly declared the new universal winner.** The mixed-promotion interpretation is the headline framing.
5. **Operational-deployment work is not recommended in this phase.** If the memo discusses paper/shadow / tiny-live as a later possibility, it is framed explicitly as a deferred future option requiring its own gate.
6. **If prior docs conflict, the conflict is surfaced explicitly.** No silent reconciliation.

## 10. Proposed files / directories

Phase 2n produces docs only:

- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-1-plan.md` — this plan, committed after Gate 2 approval.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_strategy-review-memo.md` — main strategy-review memo (sections A–J).
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n-checkpoint-report.md` — checkpoint, drafted after Gate 2 approval, immediately before commits.

No other files touched. No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `data/`, or `technical-debt-register.md` edits.

## 11. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 12. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, strategy-review memo, Gate 2 review, checkpoint report.
- **Not committed:** none — Phase 2n produces no intermediate parquet, no run output, no notebook artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 13. Safety constraints (apply throughout Phase 2n)

| Check | Requirement |
|---|---|
| Production Binance keys | none, not requested, not referenced |
| Exchange-write code | none |
| Credentials | none — no `.env`, no secrets in any artifact |
| `.mcp.json` | not created |
| Graphify | not enabled |
| MCP servers | not activated |
| Manual trading controls | none |
| Strategy logic edits | none |
| Risk engine edits | none |
| Data ingestion edits | none |
| Exchange adapter edits | none |
| Binance public URLs | none fetched |
| `.claude/settings.json` | preserved |
| Destructive git commands | none proposed |
| Changes outside working tree | none |
| New dependencies | none |
| `data/` commits | none |
| `technical-debt-register.md` edits | none (operator restriction) |
| Phase 4 work | none (operator restriction) |
| Phase 2o work | none (this is the phase that proposes 2o, not starts it) |
| Paper/shadow / tiny-live planning | none (operator restriction) |
| New backtests / variants / data | none |
| Tightening / loosening of any §10.3 / §10.4 / §11.3 / §11.6 threshold | none |
| H0 anchor preservation | enforced |
| Wave-1 result preservation | enforced (historical evidence only) |
| Phase 2l R3 PROMOTE preservation | enforced |
| Phase 2m R1a+R3 PROMOTE preservation | enforced (with strategically-mixed framing) |

## 14. Ambiguity / spec-gap items

**No new GAP entries proposed in Phase 2n.** Phase 2n carries forward existing GAPs unchanged:

- GAP-20260420-028 OPEN-LOW.
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION.
- GAP-20260420-029 RESOLVED.
- GAP-20260424-030 OPEN — disposition deferred per operator Phase 2l/2m approvals.
- GAP-20260424-031 / 032 / 033 OPEN — CARRIED.
- GAP-20260424-034 / 035 RESOLVED verification-only.
- GAP-20260424-036 RESOLVED-by-convention.

If the strategy-review surfaces a doc inconsistency that meets the bar for a permanent GAP entry (per operator restriction "If prior docs conflict, surface the conflict explicitly instead of choosing silently"), the memo will surface it but Phase 2n will NOT edit the ambiguity log unilaterally. Any GAP-log update is a separate operator-approved follow-up.

## 15. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2n. TD-016 (statistical live-performance thresholds) is informationally affected by the wave-1 + R3 + R1a+R3 results but the register itself stays untouched per operator restriction.

## 16. Proposed commit structure (end of Phase 2n)

Four commits on `phase-2n/operator-strategy-review`, after operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at **417 passed** (no code change anywhere).

1. `phase-2n: Gate 1 plan` — this file's content.
2. `phase-2n: strategy review memo` — the sections-A–J narrative.
3. `phase-2n: Gate 2 review`.
4. `phase-2n: checkpoint report`.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 17. Gate 2 review format

```
Phase: 2n — Operator / Strategy Review
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Memo sections A–J: present / complete / threshold-preserving check
Strategic-mixed-promote framing for Phase 2m: preserved verbatim
H0 anchor preservation: enforced
Recommendation: primary + fallback recorded with reasoning
What-would-change-recommendation switch conditions: present
Next-phase options analysis: present (≥ 5 options)
Non-proposal list: present
Wave-1 / Phase 2l / Phase 2m results preservation: confirmed
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 417 passed (no code change expected)
Recommended next step: operator chooses among the Phase 2o options
Questions for operator: list or "none"
```

## 18. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly. Phase 2n checkpoint includes: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 417 expected), Tests/checks failed (none expected), Known gaps (none new), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only — operator decides among Phase 2o options).

## 19. Approval gates

Two operator approvals bracket Phase 2n:

- **Gate 1 — this plan.** Approve or redirect the scope, the memo content requirements, the preservation rules, and the proposed deliverables.
- **Gate 2 — pre-commit review.** After the strategy-review memo + Gate 2 review are drafted, the operator reviews the diff + pytest output before any `git add` / `git commit`.

## 20. Post-approval execution sequence (docs-only)

After Gate 1 approval, proceed in this order and **stop before any `git add` / `git commit`**:

1. **Verify branch state.**
   ```
   git -C c:/Prometheus status --short
   git -C c:/Prometheus rev-parse --abbrev-ref HEAD
   git -C c:/Prometheus log --oneline -5
   ```
   Already on `phase-2n/operator-strategy-review` from clean main.
2. **Write this approved Gate 1 plan** to `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-1-plan.md` (this file).
3. **Draft the strategy-review memo** at `docs/00-meta/implementation-reports/2026-04-27_phase-2n_strategy-review-memo.md`, structured around §§ 6–9 of this plan plus the section-A–J content requirements.
4. **Draft Gate 2 review** at `docs/00-meta/implementation-reports/2026-04-27_phase-2n_gate-2-review.md` using the §17 format.
5. **Stop.** Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 417 passed, unchanged by docs-only edits). Do **not** run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2n checkpoint report (§18) is produced after Gate 2 approval, immediately before the commit sequence (§16).

**Awaiting operator/ChatGPT Gate 2 approval to commit, after the memo + Gate 2 review are drafted at the stop point.**
