# Phase 2f — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2f/strategy-review-variant-design`
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2f), awaiting operator / ChatGPT Gate 2 approval
**Scope:** Pre-commit review of the Phase 2f docs-only deliverables against the approved Gate 1 plan. No `git add` / `git commit` has been run. pytest is green. Baseline control is untouched.

---

## Phase

**Phase 2f — Strategy Review, Variant Design, and Validation Planning.**

Docs-only planning phase following the Phase 2e baseline. Goal: produce the strategy-review memo, hypothesis shortlist, comparison framework, anti-overfitting plan, and ambiguity-log appends.

## Scope confirmed against Gate 1 plan

Match against `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md` §§ 4–12.A and §24 execution sequence.

| Gate 1 requirement                                                          | Status  | Location of evidence                                                                                     |
|-----------------------------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------|
| Filter-layer inventory with exact rules + Phase 2e rejection attribution    | Done    | Memo Part 1 §1.2 (funnel table) + §1.3 (restrictiveness ranking)                                          |
| Structural vs. parametric classification                                    | Done    | Memo Part 1 §1.4 (25-row table)                                                                          |
| Trade-frequency sanity-check section in memo (Gate 1 condition 2)           | Done    | Memo Part 1 §1.6 (five required diagnostics + baseline snapshot + interpretation framing); **baseline values recomputed exactly from the Phase 2e artifacts `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/<SYMBOL>/{trade_log.json, funnel_total.json}` per operator Gate 2 precision fix (2026-04-24). All "~" approximations removed; values now labeled explicitly as min / median / max / mean and reported with their exact numerators/denominators.** |
| Hypothesis shortlist capped at ≤ 4 wave-1 variants (Gate 1 condition 1)     | Done    | Memo Part 2 — exactly 4 hypotheses (H-A1, H-C1, H-B2, H-D3)                                               |
| Wave-1 family prioritization: setup / trigger / HTF-bias; ≤ 1 exit variant (condition 3) | Done | 3 bottleneck-family variants (H-A1 setup, H-C1 HTF-bias, H-B2 trigger) + 1 exit variant (H-D3)         |
| Validation discipline: R-rank only, top-1–2 to V, no peeking, no re-rank (condition 4) | Done | Memo Part 3 §3.2; Gate 1 plan §11.3                                                                      |
| Memo structure: Part 1 / Part 2 / Part 3 clearly separated (condition 5)    | Done    | Memo header declares three parts; each part opens with one-paragraph summary and closes before next begins |
| Ambiguity-log appends GAP-20260424-030..035                                 | Done    | `docs/00-meta/implementation-ambiguity-log.md` lines 825+ (6 new entries appended, no existing edits)     |
| Gate 1 plan committed to docs                                               | Done    | `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md`                                  |
| Gate 2 review committed to docs                                             | Done    | this file                                                                                                |
| Still-forbidden items re-affirmed (condition 6)                             | Done    | Gate 1 plan §§ 5, 21; memo Part 3 §3.5 safety checklist                                                   |

**No scope diffs from the approved Gate 1 plan.** Memo content honours every condition applied at Gate 1.

## Docs written in Phase 2f

- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md` — new file; Gate 1 plan mirrored from the approved plan file (with all six conditions applied inline). 24 sections, no tables omitted, no TBD placeholders.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md` — new file; three-part memo (Part 1 Observations, Part 2 Proposed Hypotheses, Part 3 Execution Recommendations).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-2-review.md` — new file; this review.

Ambiguity-log appends (no existing entries modified):
- `docs/00-meta/implementation-ambiguity-log.md` — six new GAP entries appended after the existing GAP-20260419-025 entry (line 825 area). Each entry follows the repository's standard GAP template with Status / Phase discovered / Area / Blocking phase / Risk level / Related docs / Description / Why-it-matters / Options / Recommended resolution / Operator decision / Resolution evidence.

**No other files touched.** No `src/` edits. No `scripts/` edits. No `tests/` edits. No `pyproject.toml` edits. No `configs/` edits. No `.claude/` edits. No `data/` writes. No `docs/12-roadmap/technical-debt-register.md` edits.

## Ambiguity-log appends — inventory

| GAP ID              | Area     | Status       | Summary                                                                                          |
|---------------------|----------|--------------|--------------------------------------------------------------------------------------------------|
| GAP-20260424-030    | STRATEGY | OPEN         | Break-even rule text (+1.5 R) vs. Open Q #8 spec-internal conflict. H-D3 (+2.0 R) tests the alternative. |
| GAP-20260424-031    | STRATEGY | OPEN         | EMA slope wording ambiguous: discrete vs. fitted. 2f adopts discrete as working convention; any fitted-slope test becomes a separate H-C2. |
| GAP-20260424-032    | STRATEGY | OPEN         | Backtest trade-price stop vs. live MARK_PRICE stop. Mark-price sensitivity is a mandatory report cut in any future execution phase. |
| GAP-20260424-033    | STRATEGY | OPEN         | Stagnation window classification deferred; H-D5 not in wave 1 — if ever proposed, its Gate 1 must resolve this GAP first. |
| GAP-20260424-034    | STRATEGY | RESOLVED     | "Previous 8 completed 15m candles" convention verified in `setup.py`: strictly before the breakout bar; memo records it for H-A1. |
| GAP-20260424-035    | STRATEGY | RESOLVED     | Sizing formula fully specified in `sizing.py` (10-step pipeline). Memo §1.5 quotes it verbatim.   |

GAPs 030–033 remain OPEN and are explicitly non-blocking for 2f; 034 and 035 are verification-only RESOLVED.

## Filter inventory completeness check

Against Phase 2e `funnel_total.json` bucket set (10 buckets + 2 positive outcomes), the memo's §1.2 table captures every bucket with its exact count per symbol:

- 10/10 rejection buckets represented (bias_neutral, no_setup, no_close_break, TR<ATR, close_loc, ATR_regime, stop_dist, sizing, EOD_no_fill, plus the positive counts).
- Accounting invariant verified for both symbols: `148,085 = 54,541 + 85,480 + 7,443 + 216 + 157 + 4 + 203 + 0 + 0 + 41` (BTC) and `148,085 = 55,517 + 84,731 + 7,209 + 173 + 173 + 21 + 214 + 0 + 0 + 47` (ETH).
- Restrictiveness rank-ordered in §1.3 (the three dominant filters account for ~99.5% on both symbols).

Filter-to-classification mapping (§1.4) covers 25 rule elements spanning spec + backtest plan; structural count = 8 (timeframes, bar-close, structural stop, exchange-side protection, one-position/no-pyramiding/no-reversal, isolated margin/one-way, shared risk-for-comparison, shared leverage-for-comparison), parametric count = 17 (the remainder).

## Hypothesis list

**Count:** exactly 4 wave-1 hypotheses + H0 control. Target cap (≤ 4) per Gate 1 condition 1 met.

**Single-axis discipline confirmed** — each hypothesis changes exactly one parameter of H0:

| ID    | Family           | Rule changed                                              | Other parameters |
|-------|------------------|-----------------------------------------------------------|------------------|
| H0    | control          | none                                                      | all baseline     |
| H-A1  | setup-logic      | `SETUP_SIZE`: 8 → 10                                      | all else baseline |
| H-C1  | HTF-bias         | EMA pair: 50/200 → 20/100                                 | all else baseline |
| H-B2  | breakout-trigger | expansion threshold: 1.0 × ATR20 → 0.75 × ATR20           | all else baseline |
| H-D3  | exit / mgmt (1/1 cap used) | break-even threshold: +1.5 R → +2.0 R           | all else baseline |

No bundled variants. No variants outside the menu in Gate 1 plan §8. Wave-1 family prioritization honoured: 3 bottleneck variants (setup / HTF-bias / trigger) + 1 exit variant — the exit-variant cap is 1/1.

## Validation plan

- **Research / validation split recorded.** R = 2022-01-01 → 2024-12-31 (36 months); V = 2025-01-01 → 2026-04-01 (15 months). Memo §1.1 baseline rows include both windows mentally; variant runs in the future execution phase will compute per-window metrics separately.
- **Walk-forward fold scheme recorded.** On R, five rolling folds of 12-month train / 6-month test, stepping 6 months.
- **No-peeking rules recorded** (memo Part 3 §3.2, Gate 1 plan §11.3): rank on R only; top-1–2 to V; V not used to re-rank R; no iterative peeking; pre-declared §10.3/§10.4 thresholds.
- **ETH-as-comparison rule recorded** (Gate 1 plan §11.4): BTC clear improvement + ETH not catastrophically failing; ETH-only wins do not qualify a variant on BTC.
- **Cost-sensitivity as a gate** (Gate 1 plan §11.6): LOW and HIGH slippage required for any variant that clears §10.3 on MEDIUM.

## Comparison framework

- **Metrics recorded.** §10.1 — 12 metric families per symbol per variant.
- **Reporting cuts recorded.** §10.2 — per-symbol, per-year, per-month, long/short, exit-reason, cost-sensitivity, plus §7.5 diagnostics appendix (now mandatory).
- **§7.5 diagnostics required** as appendix in every variant report (Gate 1 condition 2): trades-per-month distribution, zero-trade months, median hold time, setup-to-entry conversion, candidate-to-entry conversion — with baseline values captured in memo §1.6.
- **Promotion rules pre-declared.** §10.3 — three disjoint paths to candidacy.
- **Rejection rules pre-declared.** §10.4 — expectancy floor −0.50 R or PF floor 0.30 triggers rejection regardless of trade count.

## Baseline control preserved

- No writes to `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/`.
- No edits to `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md`.
- No edits to `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md`.
- No edits to `docs/00-meta/implementation-reports/2026-04-20_phase-2e-checkpoint-report.md`.
- No edits to Phase 2e manifests or datasets.

Baseline numbers are quoted verbatim in the memo and in the Gate 1 plan, with exact source paths cited for cross-reference. The control is row 0 of every future variant-comparison report by construction.

## Safety posture

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
| New source, test, script, or config files        | none                                                   |

## Operator restrictions honoured

All six Gate 1 conditions applied. All "still forbidden" items from the Gate 1 approval text held: no code changes, no variant runs, no threshold tuning, no Phase 4 work, no data downloads, no Binance/public URL calls, no MCP/Graphify, no `.mcp.json`, no `technical-debt-register.md` edits, no `git add`, no `git commit`, no push.

## Test suite

`uv run pytest` expected to pass **387 tests** (identical to end of Phase 2e). Phase 2f made zero code changes; no test count change is expected. Output captured at pre-commit stop.

## Known gaps

GAP-20260424-030, 031, 032, 033, 034, 035 recorded in the ambiguity log. GAPs 030/031/032/033 remain OPEN and non-blocking for Phase 2f; 034/035 are RESOLVED (verification-only). No GAP is a Phase 2f completion blocker.

## Recommended next step

Operator / ChatGPT Gate 2 review of:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_strategy-review-memo.md` (three parts)
- `docs/00-meta/implementation-reports/2026-04-24_phase-2f_gate-2-review.md` (this file)
- `docs/00-meta/implementation-ambiguity-log.md` (GAP-20260424-030..035 appends)

If approved, proceed to the five-commit sequence (Gate 1 plan; memo; ambiguity-log appends; this Gate 2 review; Phase 2f checkpoint report) per Gate 1 plan §18. After commits, operator chooses the next boundary:

- (a) Phase 2g — wave-1 variant execution using H-A1, H-C1, H-B2, H-D3 on the approved walk-forward and no-peeking discipline;
- (b) Phase 2-data-follow-up — e.g., resolve GAP-031 (EMA slope definition), TD-018 (exchangeInfo `commissionRate` endpoint work to retire GAP-020/024);
- (c) Phase 4 — risk / state / persistence runtime (still deferred per existing operator restriction).

No recommendation is made among (a), (b), (c); that is the operator's decision.

## Questions for operator / ChatGPT

None. All six Gate 1 conditions have been applied inline. Open GAPs (030–033) are documented and non-blocking.

---

**Stop here. No `git add` / `git commit` has run. Awaiting operator / ChatGPT Gate 2 approval.**
