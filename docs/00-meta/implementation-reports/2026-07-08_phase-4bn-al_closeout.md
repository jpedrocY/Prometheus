# Phase 4bn-AL — Closeout

## Branch

`phase-4bn-al/longer-horizon-label-memo`

## Base SHA

`205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AK merge
closeout.)

## Phase type

Docs-only **longer-horizon label design memo** — the selected Phase 4bn-AK bounded
follow-up (`longer_horizon_label_memo`, Phase 4bn-AE §16(a)). Evaluates whether a
future longer-horizon (5m / 30m / 1h) label design is a reasonable next research
contract, compares candidate label families at the design level, and records a
decision. No data read; no label built; no namespace; no model; no rerun; no data
output; no successor execution authorized.

## Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-al_longer-horizon-label-memo.md`
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-al_closeout.md` (this file)

No source / test / script / config / manifest / gate report / sidecar / split file /
ML config / research matrix / `data/` artefact created or modified.
`current-project-state.md` left unchanged (see the report §29).

## Validation commands

- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`.
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`.
- `git checkout -b phase-4bn-al/longer-horizon-label-memo` → created at base SHA.
- `git ls-files data/microstructure/` → 0 tracked.
- `git ls-files data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git diff --check` → clean.
- `git diff --name-status main..HEAD` (after commit) → only the two Phase 4bn-AL docs
  files.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no code surface changed).

(Exact post-commit outputs in the final operator report.)

## Concise memo outcome

The single binding limitation the AJ evidence surfaced is **economic thinness at
15s** (2.47% of validation moves clear the 16 bps round-trip cost; median move
2.53 bps), on top of a demonstrated, regime-stable-within-window
**information-diagnostic** directional result (L2 +5.03 pp over majority / +2.96 pp
over persistence; block agreement 1.000; no holdout reversal). Longer horizons
(5m/30m/1h) directly target that limitation — larger raw moves, more economically
interpretable, less bounce-sensitive — but carry real, **unmeasured** risks (feature
signal decay well beyond microstructure memory, regime drift, heavy overlap /
effective-sample collapse, growing censoring near segment ends). The existing label
family (`microstructure_labels_aggtrades_v001`) covers only 1s/5s/15s/60s, so
5m/30m/1h is a **new label layer**. A **docs-only label contract / spec memo** is the
cheapest safe next step: it decides the design deliberately and pre-registers it,
commits no data/build/strategy, and defers the unmeasured empirical question to a
later separately-authorized build.

## Final AL decision

**`RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`.**

Evidence-driven, not overfit to AJ optimism and not biased toward closing: closing
would forfeit AK's cleanly-motivated selected follow-up on **unmeasured** pessimism;
insufficient-evidence does not apply because the design-level recommendation is fully
decidable from committed evidence (the unmeasured 5m/30m/1h distributions block a
*build*, not a *design memo*).

## Recommended next memo (if any)

Exactly one next **docs-only** phase: a **longer-horizon label contract / spec memo**
(design + pre-registration only; no build, no data read, no namespace). Scope:

- **Horizons:** all three at design level; **5m primary / lead**; **30m and 1h
  secondary diagnostic**.
- **Label family default:** conservative **multi-horizon diagnostic family** —
  extend strict-sign to the new horizons **and** record the continuous forward-return
  distributions + descriptive 8 bps / 16 bps cost-clearing shares (economic
  materiality as a **descriptive diagnostic**, not a baked-in target). Cost-aware
  ternary / magnitude / deadband options evaluated but **not adopted-by-default**, and
  only ever under a fixed, pre-registered, never-optimized threshold tied to the
  locked 16 bps; do-not-adopt set excluded.
- **Invariants:** carry forward every AH leakage invariant; require per-horizon
  censored-fraction reporting; preserve the AH compact-spec posture, the Phase 4bn-L
  125 GiB cap, v002/sealed-test exclusion, and the §10 dependence posture.
- **Evidence gate:** the spec memo must pre-register horizons / label policy /
  censoring / embargo / storage / claim scope, and state that any actual build or data
  read needs its **own** further separate authorization.

**No prompt generated; no successor authorized** (see below).

## Explicit boundary confirmations

- No data files read (no feature/label Parquet, no v002 terminal, no sealed test, no
  raw zip, no AH/AJ data artefact, no endpoint). ✅
- No AH builder rerun. ✅ No AI diagnostics rerun. ✅ No AJ baseline rerun. ✅
- No AJ/AI/AH metric revised, recomputed, or re-derived; every figure quoted
  verbatim. ✅
- No label built / generated; no new label or dataset namespace created or mutated;
  AH and AJ namespaces untouched. ✅
- No model / scoring / prediction / inference / new diagnostics. ✅
- No feature selection / threshold optimization / model selection / hyperparameter
  search. ✅
- No strategy / signals / PnL / backtest / Sharpe / hit-rate / position sizing /
  execution / paper / shadow / live / exchange-write. ✅
- No credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream. ✅
- No eligibility / manifest / gate / sidecar flag transition;
  `flip_research_eligible(...)` never invoked. ✅
- No empirical longer-horizon distribution invented; longer-horizon reasoning is
  design-level and qualitative only. ✅
- Nothing committed under `data/microstructure/` or `data/research/`;
  `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (§8 a/b/c) and forbidden claim scope (§8/§19) preserved
  verbatim; locked cost 8 bps/side · 16 bps round-trip preserved; the Phase 4bn-AE
  claim-scope, the Phase 4bn-AK single-follow-up selection, and every retained verdict
  and project lock preserved verbatim; the Phase 4aw always-raises invariant
  preserved (never invoked). ✅

## Remaining blockers before any label contract / build

- A **separate future operator prompt** authorizing the recommended longer-horizon
  label **contract / spec memo** (not granted here). That memo is itself **docs-only**.
- Any actual longer-horizon **label build / data generation / data read** requires a
  **further** separate authorization beyond the spec memo, and would need a budget
  preflight and preservation of the AH compact-spec posture and the Phase 4bn-L
  125 GiB cap.

## Remaining blockers before any data read / build

- No data read/build is authorized by this memo. A build would require: separate
  operator authorization; pre-registration of the exact horizon set, label policy,
  censoring/embargo/storage, and leakage invariants (per the recommended spec memo);
  and preservation of v002/sealed-test exclusion (`test_rows_loaded = 0`,
  `v002_terminal_window_read = false`, `sealed_test_split_touched = false`).

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility
memo** clearing: M0.5 cost realism at 8 bps/side · 16 bps round-trip; execution
feasibility; slippage/spread (which aggTrades-only data cannot support — mid/book
required, and the `bookticker_midprice_data_admissibility_memo` remains deferred and
unauthorized); label economic relevance (the 15s strict-sign target is non-economic,
and no longer-horizon label result would by itself establish tradability); strategy
admissibility vs the retained rejections and the M0 §7.D microstructure-lane
`NOT_RECOMMENDED_NOW` posture; the Phase 4al no-rescue constraints — **plus** separate
operator authorization for each of strategy / signals / PnL / backtest / paper-shadow
/ live / exchange-write. No AL/AK/AJ result softens this boundary.

## Recommended state

**Remain paused.** The longer-horizon label memo is recorded and recommends exactly
one next docs-only label contract / spec memo (5m/30m/1h at design level; 5m primary;
conservative multi-horizon diagnostic family default). The recommended memo is **not
started** and awaits a separate future operator prompt.

## Result state

`LONGER_HORIZON_LABEL_MEMO_RECORDED__LABEL_CONTRACT_MEMO_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Explicit no-successor execution statement

Phase 4bn-AL authorizes **no** successor execution phase. It does not generate the
recommended memo's prompt; it does not write, build, or generate any longer-horizon
label or label layer; it does not create any label/dataset namespace; it does not
read any feature/label Parquet / v002 terminal / sealed test / raw zip / AH / AJ data
artefact; it does not acquire data or call any endpoint; it does not train / score /
predict / infer, run diagnostics, do feature selection / threshold optimization /
model selection / hyperparameter search, or rerun the AH builder / AI diagnostics /
AJ baselines; it does not do strategy / signals / PnL / backtest / paper-shadow /
live-readiness / deployment / exchange-write; and it does not authorize any Phase 5 /
successor phase. The recommended longer-horizon label contract / spec memo begins only
under a separate future operator prompt. Do not merge to main and do not push unless
explicitly instructed in a later prompt; do not generate a merge-closeout or the
recommended next prompt unless explicitly instructed later.
