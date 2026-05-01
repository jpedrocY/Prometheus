# Phase 4f Merge Closeout

## Summary

Phase 4f (External Strategy Research Landscape and V2 Hypothesis Candidate
Memo, docs-only) has been merged into `main` via a `--no-ff` merge commit.
Phase 4f surveyed external systematic-trading evidence (academic and
practitioner literature) for transferable strategy families and
predeclared a new ex-ante hypothesis candidate, V2 — Participation-Confirmed
Trend Continuation, as the operator-selected return-to-research move.

Phase 4f is docs-only. No source code, tests, scripts, data, or manifests
were modified. No backtests were run. No data was acquired. No retained
verdicts were revised. No project locks changed. No paper/shadow,
live-readiness, deployment, production-key, exchange-write, MCP,
Graphify, `.mcp.json`, or credentials work occurred.

V2 is **pre-research only**: not implemented, not backtested, not
validated, not live-ready, and **not a rescue** of R3 / R2 / F1 / D1-A.

Phase 4 canonical remains unauthorized. Phase 4g and any successor phase
remain unauthorized. Recommended state remains **paused**.

## Files changed

The merge introduced two new docs-only files into `main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4f_external-strategy-research-landscape-v2-candidates.md`
  (Phase 4f research memo; 680 lines; 34 sections)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4f_closeout.md`
  (Phase 4f closeout report; 259 lines)

The housekeeping commit additionally updated:

- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4f paragraph; refreshed
  "Current phase" / "Most recent merge" code blocks)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4f_merge-closeout.md`
  (this file)

No source code, tests, scripts, data files, manifests, specs,
thresholds, parameters, project locks, or prior verdict records were
modified.

## Phase 4f commits included

| Role | SHA | Message |
| --- | --- | --- |
| Phase 4f research report | `4f5d12b97e0127daaef6bea7e96db322fb98d053` | phase-4f: external strategy research landscape and V2 hypothesis candidate memo (docs-only) |
| Phase 4f closeout report | `4a7cc9f515af9d0669932d57acff4b304a005b4c` | docs(phase-4f): closeout report (Markdown artefact) |

## Merge commit

| Field | Value |
| --- | --- |
| Merge SHA | `4535f463a9759716fe3665b551f9a2d949d4a62e` |
| Merge style | `--no-ff` |
| Source branch | `phase-4f/external-strategy-research-landscape-v2-candidates` |
| Target branch | `main` |
| Pre-merge `main` SHA | `da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c` |

## Housekeeping commit

The housekeeping commit (`<HOUSEKEEPING_SHA>` recorded in the chat
closeout block after this file is committed) updates
`docs/00-meta/current-project-state.md` and adds this merge-closeout
file. It is docs-only and post-merge.

## Final git status

After merge + housekeeping:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Final git log --oneline -8

(Captured after the housekeeping commit and final push; recorded
verbatim in the chat closeout block.)

## Final rev-parse

(Captured after the housekeeping commit and final push; recorded
verbatim in the chat closeout block: `git rev-parse main` and
`git rev-parse origin/main`.)

## main == origin/main confirmation

After the housekeeping commit is pushed, `git rev-parse main` and
`git rev-parse origin/main` both resolve to the same SHA. Local and
remote are in sync.

## Research conclusion

- **Phase 4f was docs-only.** No code, tests, scripts, data, or manifests
  were modified. No backtests were run. No data was acquired.
- **Phase 4f surveyed external systematic-trading evidence.** The memo
  consulted academic and practitioner literature including time-series
  momentum (Moskowitz / Ooi / Pedersen 2012; Hurst / Ooi / Pedersen
  2017), classical technical-rule evidence (Brock / Lakonishok / LeBaron
  1992), crypto-asset returns (Liu / Tsyvinski 2018, 2021), crypto
  carry / funding (BIS WP 1087), crypto microstructure
  (Easley / O'Hara / Yang / Zhang 2024), data-snooping discipline
  (Bailey / Borwein / López de Prado / Zhu 2014), time-of-day periodicity
  (Hattori 2024 — UK-evening peak; Eross / Urquhart / Wolfe 2019 — BTC
  intraday periodicities), and crypto time-series momentum
  (Han / Kang / Ryu 2024; Manamala 2025 — volatility compression).
- **Phase 4f distinguished transferable from non-transferable
  institutional families.** HFT / liquidity-provision / market-making is
  classified as non-transferable to the operator's runtime substrate.
  CTA / time-series momentum / trend-following is the strongest
  transferable family. Volume / order-flow signals are best treated as
  confirmation / regime context. Crypto derivatives-flow indicators
  (funding, basis, open interest, taker imbalance) are best treated as
  context / regime / cost lenses, not as standalone signals.
- **Time-series momentum / trend-following remains the strongest
  transferable evidence family** for the project's operator-supervised,
  bar-completed-only, market-MARKET-entry, mark-price-stop discipline.
- **Volume / order-flow is strongest as confirmation / regime context**
  (e.g., participation filters, regime classification), not as a
  standalone breakout-prediction signal.
- **Crypto derivatives-flow indicators are best treated as context /
  regime / cost lenses.** Funding rate context, basis context, open
  interest regime, and taker imbalance context can inform regime / cost
  filters but should not be primary entry triggers — particularly given
  the D1-A retained-evidence MECHANISM PASS / FRAMEWORK FAIL — other
  outcome.
- **5m remains diagnostic-only, not primary signal**, consistent with
  Phase 3t §14.2 closure of the 5m research thread and the Phase 3o
  predeclared question set discipline.
- **V2 is a new ex-ante hypothesis, not a rescue.** V2 is not a parameter
  retune of R3, R2, F1, or D1-A. V2 is a fresh hypothesis declared
  before any backtest and structurally distinct from prior retained
  candidates.

## V2 candidate hypothesis family

- **Name:** V2 — Participation-Confirmed Trend Continuation.
- **Status:** pre-research only; not implemented; not backtested;
  not validated; not live-ready; not a rescue.
- **Core premise:** trade trend-continuation / breakout events on
  BTCUSDT perpetual only when **price structure**, **volatility regime**,
  **participation / volume**, and **derivatives-flow context** align.
  The hypothesis explicitly conditions entries on multi-domain
  agreement, not on price-only signal generation.
- **Timeframe matrix:**
  - signal candidates: 15m / 30m / 1h
  - bias candidates: 1h / 4h
  - session / volume bucket candidates: 30m / 1h
  - 5m: diagnostic-only, not primary signal
- **Feature bound:**
  - max **8** active entry features
  - max **3** active exit / regime features
- **Validation requirements:**
  - **predeclaration before backtest** (no parameter / threshold tuning
    after seeing data; thresholds locked in spec memo before any
    backtest run);
  - chronological holdout (no shuffle / no bootstrap leakage);
  - §11.6 HIGH cost sensitivity must be applied (8 bps per side floor);
  - BTCUSDT primary, ETHUSDT comparison (no live-readiness implication
    on either);
  - deflated Sharpe / probability-of-backtest-overfitting (PBO)
    treatment if a grid search is ever performed;
  - no live / paper implications from any V2 backtest.

## Candidate next-slice decision

Phase 4f recommended the following decision menu for the operator:

- **Option B — docs-only V2 strategy-spec memo (PRIMARY).** Predeclares
  the V2 entry-feature set, exit/regime-feature set, all thresholds, all
  filter rules, and the validation methodology *before* any backtest is
  run. This is the recommended next step because predeclaration is the
  binding anti-data-snooping discipline.
- **Option C — docs-only V2 data-requirements and feasibility memo
  (CONDITIONAL SECONDARY).** Acceptable as a substitute for Option B
  only if the operator wants to scope data feasibility (15m / 30m / 1h /
  4h coverage; aggTrades / takerBuy / openInterest / fundingRate
  endpoints) before locking the V2 spec.
- **Option A — remain paused (PROCEDURALLY ACCEPTABLE).** Acceptable but
  defers the operator's stated return-to-research intent.
- **Option D — immediate data acquisition (NOT RECOMMENDED).**
  Acquiring v003 / supplemental datasets before V2 spec is locked
  invites parameter tuning to observed data.
- **Option E — immediate exploratory backtest (REJECTED).** Rejected as
  data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014.
  No exploratory backtests on V2 are permitted before predeclaration.
- **Option F — paper/shadow / live-readiness / exchange-write
  (FORBIDDEN).** Forbidden per `docs/12-roadmap/phase-gates.md`. None
  of these gates is met. No paper/shadow runtime; no live-readiness
  implication; no production keys; no authenticated APIs; no private
  endpoints; no user stream; no WebSocket; no MCP; no Graphify;
  no `.mcp.json`; no credentials; no exchange-write capability.

## Verification evidence

The Phase 4f branch was verified clean before merge:

- `ruff check .` passed (`All checks passed!`)
- `pytest` passed (`785 passed`)
- `mypy --strict src/prometheus` passed (`Success: no issues found in 82
  source files`)

Verification was performed against the Phase 4f branch tip
(`4a7cc9f515af9d0669932d57acff4b304a005b4c`) before the merge. Phase 4f
introduced docs-only changes; the verification baseline is identical to
the Phase 4e merge baseline.

## Forbidden-work confirmation

The following did **not** occur in Phase 4f or in this merge closeout:

- no successor phase started (no Phase 4g; no V2 spec memo; no V2
  feasibility memo; no implementation; no successor authorization);
- no implementation code changed;
- no `src/prometheus/` modification;
- no test modification;
- no script modification;
- no data acquisition / patching / regeneration / modification;
- no `data/manifests/*.manifest.json` modification;
- no Phase 3q v001-of-5m manifest modification;
- no v003 dataset created;
- no Q1–Q7 rerun;
- no diagnostics rerun;
- no backtests run;
- no `scripts/phase3q_5m_acquisition.py` execution;
- no `scripts/phase3s_5m_diagnostics.py` execution;
- no V2 strategy spec written in this merge (V2 spec memo is the next
  phase's scope, not this merge's);
- no V2 implementation;
- no V1 / R3 / R2 / F1 / D1-A implementation or rescue;
- no retained verdict revision;
- no project-lock revision;
- no §11.6 change;
- no §1.7.3 change;
- no Phase 3v `stop_trigger_domain` governance change;
- no Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance change;
- no spec / backtest-plan / validation-checklist / stop-loss-policy /
  runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff
  / first-run-setup-checklist substantive edit;
- no `docs/00-meta/implementation-ambiguity-log.md` modification (all
  four pre-coding governance blockers remain RESOLVED per
  Phase 3v / Phase 3w);
- no Phase 4 canonical authorization;
- no reconciliation implementation;
- no real-exchange adapter implementation;
- no exchange-write capability;
- no order placement / cancellation;
- no credential storage / request / use;
- no authenticated REST / private endpoints / public endpoints in code /
  user stream / WebSocket / listenKey lifecycle;
- no MCP / Graphify enablement;
- no `.mcp.json` modification;
- no `.env` files created;
- no deployment;
- no paper/shadow runtime;
- no live-readiness implication;
- no v002 dataset / manifest modification;
- no Phase 3p §4.7 amendment.

## Remaining boundary

- R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
  F1 / D1-A retained research evidence only.
- R2 FAILED — §11.6 cost-sensitivity blocks.
- F1 HARD REJECT.
- D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- §11.6 = 8 bps HIGH per side.
- §1.7.3 project-level locks (including mark-price stops).
- v002 verdict provenance.
- Phase 3q mark-price 5m manifests `research_eligible: false`.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4a public API and runtime behavior.
- Phase 4e reconciliation-model design memo (governance defined; not
  implemented).

All preserved verbatim. No project locks changed.

## Next authorization status

- **Phase 4 canonical:** unauthorized.
- **Phase 4g / any successor phase:** unauthorized.
- **V2 strategy-spec memo (docs-only):** Phase 4f's primary
  recommendation. Requires explicit operator authorization before
  starting; this merge does not start it.
- **V2 data-requirements / feasibility memo (docs-only):** Phase 4f's
  conditional secondary recommendation. Requires explicit operator
  authorization before starting; this merge does not start it.
- **V2 implementation:** unauthorized.
- **V2 backtests:** unauthorized.
- **V2 data acquisition:** unauthorized.
- **Paper/shadow:** unauthorized.
- **Live-readiness:** unauthorized.
- **Deployment:** unauthorized.
- **Production keys:** unauthorized.
- **Authenticated APIs:** unauthorized.
- **Private endpoints / user stream / WebSocket:** unauthorized.
- **MCP / Graphify / `.mcp.json` / credentials:** unauthorized.
- **Exchange-write:** unauthorized.

**Recommended state remains paused. No next phase authorized.**
