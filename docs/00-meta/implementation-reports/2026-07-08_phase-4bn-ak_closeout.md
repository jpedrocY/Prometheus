# Phase 4bn-AK — Closeout

## Branch

`phase-4bn-ak/ml-arc-decision-memo`

## Base SHA

`3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AJ merge
closeout).

## Phase type

Docs-only ML **arc-decision** memo. Reviews the completed Phase 4bn-AH / 4bn-AI /
4bn-AJ evidence, applies the pre-registered Phase 4bn-AE §16/§17/§18 arc-decision
framework, records the arc decision. No data read; no model; no rerun; no data
output; no namespace mutation; no successor execution authorized.

## Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_closeout.md` (this file)

No source / test / script / config / manifest / gate report / sidecar / split file
/ ML config / research matrix / `data/` artefact created or modified.
`current-project-state.md` left unchanged (see the report §29).

## Validation commands

- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`.
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`.
- `git ls-files data/microstructure/` → 0 tracked.
- `git ls-files data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git diff --check` → clean.
- `git diff --name-status main..HEAD` (after commit) → only the two Phase 4bn-AK
  docs files.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no code surface changed).

(Exact post-commit outputs in the final operator report.)

## Concise decision outcome

The pre-registered Phase 4bn-AE §16 continue gates are **all** satisfied on the
recorded Phase 4bn-AJ evidence (accuracy +5.03 pp over majority / +2.96 pp over
persistence; macro-F1 +0.145 over the majority floor; validation date- and
month-block agreement 1.000; holdout no sign reversal; high-confidence tail 0.633 >
floor 0.4950 though overconfident; cost acknowledged non-economic at 15s). No KILL
clause fires. The macro-F1 caveat (persistence 0.402 > L2 0.366) is a pre-anticipated
degenerate-flat-class artifact that the majority-referenced §16 gate does not treat
as disqualifying; its stricter `INVESTIGATE_AMBIGUOUS` reading routes to this same
AK memo under §17/§18 and resolves the same way. The arc is therefore continued to
**exactly one** bounded follow-up.

## Final AK decision

**`CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`.**

## Selected follow-up

**Exactly one: category 1 — `longer_horizon_label_memo` (Phase 4bn-AE §16(a)): a
longer-horizon (5m/30m/1h) label memo.** Rationale: the single binding limitation
the AJ evidence surfaced is economic thinness at 15s (2.47% of moves clear the
16 bps round-trip cost); §9 names longer horizons as "where cost could plausibly be
cleared"; it is the most responsive, most bounded, lowest-cost single next docs
step, and stays within the existing aggTrades label lineage (no new data source).

**Not started.** The selected follow-up requires a **separate future operator
prompt** before any work begins. This memo authorizes no implementation, label
build, data generation, data read, or successor execution phase.

**Other three §16 categories explicitly rejected / deferred:**
`bookticker_midprice_data_admissibility_memo` (§16(b), premature before
longer-horizon materiality; heavier new-data path); `code_only_evaluation_framework_
extension`/block-bootstrap (§16(c), polish over already-maximal 1.000 block
agreement; does not touch the economic constraint); `fixed_capacity_model_comparison_
memo` (§16(d), capacity is not the evidenced bottleneck; highest model-shopping
risk).

## Explicit boundary confirmations

- No data files read (no feature/label Parquet, no v002 terminal, no sealed test,
  no raw zip, no AH/AJ data artefact, no endpoint). ✅
- No AH builder rerun. ✅ No AI diagnostics rerun. ✅ No AJ baseline rerun. ✅
- No AJ metric revised, recomputed, or re-derived; every figure quoted verbatim. ✅
- No model / scoring / prediction / inference / new diagnostics. ✅
- No feature selection / threshold optimization / model selection / hyperparameter
  search. ✅
- No dataset/baseline namespace created or mutated; AH and AJ namespaces untouched. ✅
- No strategy / signals / PnL / backtest / Sharpe / hit-rate / position sizing /
  execution / paper / shadow / live / exchange-write. ✅
- No credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream. ✅
- No eligibility / manifest / gate / sidecar flag transition;
  `flip_research_eligible(...)` never invoked. ✅
- Nothing committed under `data/microstructure/` or `data/research/`;
  `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (§8 a/b/c) and forbidden claim scope (§8/§19) preserved
  verbatim; locked cost 8 bps/side · 16 bps round-trip preserved; every retained
  verdict and project lock preserved verbatim. ✅

## Remaining blockers before the selected follow-up (longer-horizon label memo)

- A **separate future operator prompt** explicitly authorizing the longer-horizon
  label memo (not granted here).
- The follow-up is itself a **docs-only memo** when authorized; any actual
  longer-horizon **label build / data generation / data read** would require its own
  further separate authorization beyond that memo.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility
memo** clearing: M0.5 cost realism at 8 bps/side · 16 bps round-trip; execution
feasibility; slippage/spread (which aggTrades-only data cannot support — mid/book
data required); label economic relevance (the 15s strict-sign target is
non-economic); strategy admissibility vs the retained rejections and the M0 §7.D
microstructure-lane `NOT_RECOMMENDED_NOW` posture; the Phase 4al no-rescue
constraints — **plus** separate operator authorization for each of strategy /
signals / PnL / backtest / paper-shadow / live / exchange-write. No AK or AJ result
softens this boundary.

## Recommended state

**Remain paused.** ML arc decision recorded (continue to exactly one bounded
follow-up); the selected longer-horizon label memo is **not started** and awaits a
separate future operator prompt.

## Result state

`ML_ARC_DECISION_RECORDED__EXACTLY_ONE_BOUNDED_FOLLOWUP_SELECTED__NO_STRATEGY__FOLLOWUP_NOT_STARTED__REMAIN_PAUSED`

## Explicit no-successor execution statement

Phase 4bn-AK authorizes **no** successor execution phase. It does not implement,
run, or start any follow-up; it does not create the selected follow-up's prompt; it
does not authorize any label build, data generation, data read, ML, diagnostics,
strategy, signals, PnL, backtest, paper/shadow, live-readiness, deployment,
exchange-write, or any Phase 5 / successor phase. The selected longer-horizon label
memo begins only under a separate future operator prompt. Do not merge to main and
do not push unless explicitly instructed in a later prompt; do not generate a
merge-closeout or the selected follow-up prompt unless explicitly instructed later.
