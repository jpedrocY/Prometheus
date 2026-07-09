# Phase 4bn-AM — Closeout

## Branch

`phase-4bn-am/longer-horizon-label-contract-spec`

## Base SHA

`4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AL merge
closeout.)

## Phase type

Docs-only **longer-horizon label contract / specification memo** — the memo
recommended by Phase 4bn-AL. Defines a prospective longer-horizon (5m / 30m / 1h)
aggTrades label layer at the design level and records a build recommendation. No data
read; no label built; no namespace created/mutated; no model; no rerun; no source/test
change; no successor execution authorized.

## Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-am_longer-horizon-label-contract-spec.md`
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-am_closeout.md` (this file)

No source / test / script / config / manifest / gate report / sidecar / split file /
ML config / research matrix / `data/` artefact created or modified.
`current-project-state.md` left unchanged (see the report §34).

## Validation commands

- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`.
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`.
- `git checkout -b phase-4bn-am/longer-horizon-label-contract-spec` → created at base
  SHA.
- `git ls-files data/microstructure/` → 0 tracked.
- `git ls-files data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git diff --check` → clean.
- `git diff --name-status main..HEAD` (after commit) → only the two Phase 4bn-AM docs
  files.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no code surface changed).

(Exact post-commit outputs in the final operator report.)

## Concise contract / spec outcome

A safe, precise longer-horizon label contract is definable from committed evidence.
The memo pre-registers a **new sibling label family**
`microstructure_labels_longhorizon_aggtrades_v001` (the frozen v002 family cannot be
mutated — its horizon set is asserted `("1s","5s","15s","60s")`), reusing the v002
schema pattern for horizons **5m (300000 ms, lead) / 30m (1800000 ms) / 1h
(3600000 ms)**: regression `forward_log_return_H` + classification
`forward_direction_H` columns, per-horizon `reference_row_index_H` /
`reference_timestamp_ms_H` / `horizon_censored_flag_H` support, global invalid/any-
censored flags, 17 lineage columns + `label_config_hash`. Direction policy = **strict
sign extension** (no deadband / no bp threshold / no optimization / no cost-fitting);
cost-aware / magnitude / neutral-band options **evaluated but not adopted** (any future
use must be fixed, pre-registered, cost-locked, separately authorized). A future build
must report **descriptive** continuous-return / cost-clearing (8 bps / 16 bps) summaries
per horizon × split, preserve every AH leakage invariant (completed-event target;
past-only features; chrono split + 1-day embargo; per-horizon envelope-terminal
censoring with the censored fraction measured and growing with H; v002/sealed-test
exclusion; `test_rows_loaded = 0`), preserve the AH compact-spec posture and the
Phase 4bn-L 125 GiB cap (budget preflight), write to a local/gitignored namespace under
Phase 4bb-F sidecar policy, and keep all non-authorization flags `false`.

## Final AM decision

**`LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED`.**

Evidence-driven: `LABEL_CONTRACT_SPEC_BLOCKED` does not apply (a safe contract is
definable from committed source); `NO_BUILD_RECOMMENDED` would dead-end the
longer-horizon line without a safety justification (the build is bounded, descriptive,
and answers exactly the economic-materiality question AK/AL identified). So the memo
records the contract and **recommends** — but does not authorize — a future, separately
authorized label-build phase.

## Recommended future build authorization (if any)

Exactly one future **label-build authorization phase** (build the
`microstructure_labels_longhorizon_aggtrades_v001` layer for 5m/30m/1h over the
admitted pre-v002 aggTrades segment only, single controlled run with one-run guard;
compact label Parquet + sidecars + manifest + leakage/split/censoring proof + §17
descriptive summaries; every leakage invariant preserved; v002/sealed-test excluded;
non-authorization flags all false). ML / diagnostics / strategy explicitly excluded;
evaluation of the built labels is a **further** separate authorization.

**No prompt generated; no build authorized.** The build begins only under a separate
future operator prompt and may read data only under that prompt.

## Explicit boundary confirmations

- No data files read (no feature/label Parquet, no v002 terminal, no sealed test, no
  raw zip, no AH/AJ data artefact, no endpoint). ✅
- No label built or generated; no label/dataset/output namespace created or mutated;
  AH/AJ namespaces untouched. ✅
- No AH builder rerun. ✅ No AI diagnostics rerun. ✅ No AJ baseline rerun. ✅
- No AJ/AI/AH metric revised, recomputed, or re-derived; every figure quoted
  verbatim. ✅
- No model / scoring / prediction / inference / new diagnostics. ✅
- No feature selection / threshold optimization / model selection / hyperparameter
  search. ✅
- No source / test / manifest / gate / sidecar / split / ML-config change. ✅
- No cost-aware / magnitude / deadband label adopted; strict-sign default only. ✅
- No empirical longer-horizon distribution invented; longer-horizon content is
  design-level and qualitative only. ✅
- No strategy / signals / PnL / backtest / Sharpe / hit-rate / position sizing /
  execution / paper / shadow / live / exchange-write. ✅
- No credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream. ✅
- No eligibility / authorization / manifest / gate / sidecar flag transition;
  `flip_research_eligible(...)` never invoked. ✅
- Nothing committed under `data/microstructure/` or `data/research/`;
  `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (§8 a/b/c) and forbidden claim scope (§8/§19) preserved
  verbatim; locked cost 8 bps/side · 16 bps round-trip preserved; the Phase 4bn-AE
  claim-scope, the Phase 4bn-AK single-follow-up selection, the Phase 4bn-AL
  no-build/no-data-read boundary, and every retained verdict and project lock preserved
  verbatim. ✅

## Remaining blockers before any label build

- A **separate future operator prompt** authorizing the label-build phase (not granted
  here).
- That build must: read data only under that prompt; preserve every §18 leakage
  invariant and the compact-spec / 125 GiB-cap posture (with budget preflight); write
  only to a local/gitignored namespace; keep all non-authorization flags `false`; and
  commit no data files.

## Remaining blockers before any data read / build

- No data read/build is authorized by this memo. A build requires separate operator
  authorization and pre-registration compliance (§13–§20), and must preserve
  v002/sealed-test exclusion (`test_rows_loaded = 0`, `v002_terminal_window_read =
  false`, `sealed_test_split_touched = false`).

## Remaining blockers before any ML / diagnostics

- Building the longer-horizon label layer is **not** permission to model it. Any ML
  training, scoring, prediction, inference, or diagnostics over the built labels
  requires its **own further separate authorization** beyond the build phase; all
  non-authorization flags remain `false` until then.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (AE §19). A separate future **M0-style mechanism-admissibility memo** clearing:
M0.5 cost realism at 8 bps/side · 16 bps round-trip; execution feasibility;
slippage/spread (which aggTrades-only data cannot support — mid/book required, and the
`bookticker_midprice_data_admissibility_memo` remains deferred and unauthorized); label
economic relevance (no longer-horizon label result by itself establishes tradability);
strategy admissibility vs the retained rejections and the M0 §7.D microstructure-lane
`NOT_RECOMMENDED_NOW` posture; the Phase 4al no-rescue constraints — **plus** separate
operator authorization for each of strategy / signals / PnL / backtest / paper-shadow /
live / exchange-write. No AM/AL/AK/AJ result softens this boundary.

## Recommended state

**Remain paused.** The longer-horizon label contract / spec is recorded and recommends
exactly one future, separately authorized label-build phase. The recommended build is
**not started** and awaits a separate future operator prompt.

## Result state

`LONGER_HORIZON_LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Explicit no-successor execution statement

Phase 4bn-AM authorizes **no** successor execution phase. It does not generate the
recommended build phase's prompt; it does not build, generate, or write any
longer-horizon label or label layer; it does not create any label/dataset/output
namespace; it does not read any feature/label Parquet / v002 terminal / sealed test /
raw zip / AH / AJ data artefact; it does not acquire data or call any endpoint; it does
not change any source / test / manifest / gate / sidecar / split / ML config; it does
not train / score / predict / infer, run diagnostics, do feature selection / threshold
optimization / model selection / hyperparameter search, or rerun the AH builder / AI
diagnostics / AJ baselines; it does not do strategy / signals / PnL / backtest /
paper-shadow / live-readiness / deployment / exchange-write; and it does not authorize
any Phase 5 / successor phase. The recommended label-build phase begins only under a
separate future operator prompt. Do not merge to main and do not push unless explicitly
instructed in a later prompt; do not generate a merge-closeout or the recommended next
prompt unless explicitly instructed later.
