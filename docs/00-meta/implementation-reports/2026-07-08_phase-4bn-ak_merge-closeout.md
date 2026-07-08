# Phase 4bn-AK — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AK — ML Arc Decision Memo. Branch: `phase-4bn-ak/ml-arc-decision-memo`.

## 2. Phase type

Docs-only ML **arc-decision** memo; **merge-only review** (this closeout). No code,
no data read, no rerun, no namespace mutation, no successor execution.

## 3. Base SHA

`3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`
(`docs(phase-4bn-aj): finalize merge closeout shas`; the pre-AK `main` tip).

## 4. Pre-merge branch HEAD

`608eca8abf49c9dcb546bde5439f79627aecf12f`
(`docs(phase-4bn-ak): record ml arc decision memo`).

## 5. Main / origin main before merge

`main == origin/main == 3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0` (verified in sync
before merge).

## 6. Summary of the Phase 4bn-AK decision memo

Phase 4bn-AK reviewed the completed Phase 4bn-AH (data-reading dataset builder +
single run), 4bn-AI (descriptive diagnostics, no models), and 4bn-AJ (fixed
baseline run + verdict `CONTINUE_ONE_FOLLOWUP`) evidence, recovered the
pre-registered Phase 4bn-AE §16/§17/§18 arc-decision framework exactly, and applied
it. All six frozen §16 CONTINUE gates are satisfied on the recorded AJ evidence
(validation accuracy +5.03 pp over the majority floor / +2.96 pp over persistence;
macro-F1 +0.145 over the majority floor; validation date- and month-block agreement
1.000; holdout no sign reversal; high-confidence tail 0.633 > majority floor 0.4950
though overconfident in level; cost acknowledged non-economic at 15s), and **no**
KILL clause fires. The macro-F1 caveat (persistence 0.402 > L2 0.366) is a
pre-anticipated degenerate-flat-class artifact; the §16 macro-F1 gate is
majority-referenced (per the KILL clause and the "+0.14" v002 anchor), which L2
clears, and the stricter `INVESTIGATE_AMBIGUOUS` reading routes under §17/§18 to the
same AK memo and resolves identically. AK therefore records
`CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP` and selects exactly one bounded follow-up.

## 7. Confirmation AK was docs-only

Confirmed. The branch adds exactly two Markdown files under
`docs/00-meta/implementation-reports/` and modifies nothing else. No source, test,
script, config, manifest, gate report, sidecar, split file, ML config, research
matrix, model binary, row-level prediction, or `data/` artefact was created or
modified. `git diff --name-status main..phase-4bn-ak/ml-arc-decision-memo` shows
two `A` (added) docs files and no `M`.

## 8. Confirmation current-project-state.md was left unchanged, and why

Confirmed unchanged. The update convention at this point in the arc is **not
clear/consistent**: the docs-only decision memos Phase 4bn-AE and 4bn-AG each added
a `current-project-state.md` paragraph, but the three most recent phases — Phase
4bn-AH, 4bn-AI, and 4bn-AJ (including the AJ verdict phase, the immediate
predecessor) — did **not** (no paragraph exists for any of them, and their
tracked-file lists exclude the state doc). The state doc is additionally flagged by
the Phase 4bn-AE external review as an oversized/stale single-source-of-truth
pending a consolidation memo. Per the operator instruction ("if there is no clear
current-project-state update convention for this point, do not update it; record
that it remains unchanged") and matching the immediate AH/AI/AJ precedent, Phase
4bn-AK recorded the arc decision **only** in the report + closeout and left
`current-project-state.md` untouched.

## 9. Final AK decision

`CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`.

## 10. Selected follow-up

Exactly one: category 1 — `longer_horizon_label_memo` (Phase 4bn-AE §16(a)): a
longer-horizon (5m / 30m / 1h) label memo.

## 11. Confirmation the selected follow-up is not started

Confirmed. Phase 4bn-AK selected the follow-up **only**; it did not implement, run,
or begin it, did not build any label layer, generated no data, read no data, and
created no follow-up prompt.

## 12. Confirmation the selected follow-up requires separate future operator authorization

Confirmed. Per Phase 4bn-AE §16/§18, the selected longer-horizon label memo requires
a **separate future operator prompt** before any work begins. Neither Phase 4bn-AK
nor this merge authorizes it.

## 13. Explicit rejection / deferral of the other three follow-up categories

The other three §16 categories are explicitly rejected / deferred and are **not**
authorized by AK or this merge:

- `bookticker_midprice_data_admissibility_memo` (§16(b)) — bookTicker / mid-price
  data-admissibility memo;
- `code_only_evaluation_framework_extension` (§16(c)) — block-bootstrap / code-only
  evaluation-framework extension;
- `fixed_capacity_model_comparison_memo` (§16(d)) — one fixed-capacity
  model-comparison memo.

Selecting one follow-up consumes the single-follow-up budget; only the
longer-horizon label memo is licensed, and only via a separate future operator
prompt.

## 14. Summary of why the longer-horizon label memo was selected

- Phase 4bn-AJ established **real short-horizon directional information** (L2 clears
  both statistical floors, stably across every validation block, with no
  overfitting; reproduces the v002 small-lift sign).
- The single **binding limitation** is **economic thinness at 15s**: the 15s
  strict-sign target is non-economic by design (§9).
- Only **2.47%** of validation 15s moves clear the locked **16 bps** round-trip cost
  (1.20% holdout; median |return| 2.53 bps) — the horizon is almost never
  economically relevant.
- Phase 4bn-AE §9 names longer horizons as "where cost could plausibly be cleared
  and are the correct subject of a future label memo." A longer-horizon label memo
  is the **most responsive, most bounded, lowest-cost** docs-only next question, and
  stays within the existing aggTrades label lineage (no new data source), unlike the
  three deferred categories.

## 15. Preserved allowed claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_ALLOWED`):

- the 45 causal aggTrades features contain **short-horizon directional information**
  about `forward_direction_15s` on the pre-v002 segment;
- the **directional sign** of the v002 small-lift result **is reproduced** on the
  larger, earlier pre-v002 regime;
- the calibration / confidence tail **beats the majority floor** on accuracy but is
  **overconfident in level** — usable for ranking / diagnostic reading only, not as
  calibrated probabilities.

## 16. Preserved forbidden claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing in AK
or this merge may be cited as evidence of: tradability; profitability;
strategy/execution viability; slippage/spread adequacy; live/paper-shadow readiness;
PnL; backtest validity; production suitability; economic significance. The
2.47%-of-moves-clear-cost figure is descriptive context, **not** edge. The locked
cost reference remains **8 bps per side / 16 bps round-trip**.

## 17. Confirmation no data files were read during AK or the merge review

Confirmed. Phase 4bn-AK and this merge review read **no** feature/label Parquet row,
**no** v002 terminal window, **no** sealed test split, **no** raw zip, **no** AH/AJ
local result artefact under `data/research/` or `data/microstructure/`, and called
**no** endpoint. All evidence was recovered from committed Markdown and committed
source constants.

## 18. Confirmation no AH builder rerun occurred

Confirmed. The Phase 4bn-AH data-reading dataset builder was not re-run; its one-run
guard and output namespace were untouched.

## 19. Confirmation no AI diagnostics rerun occurred

Confirmed. The Phase 4bn-AI descriptive diagnostics were not re-run.

## 20. Confirmation no AJ baseline rerun occurred

Confirmed. The Phase 4bn-AJ fixed baseline runner (majority / persistence / L2) was
not re-run; no baseline was fit, scored, or evaluated.

## 21. Confirmation no AJ metrics were revised, recomputed, or re-derived

Confirmed. Every AJ figure was quoted verbatim from the committed AJ verdict report;
none was revised, recomputed, or re-derived.

## 22. Confirmation no model / scoring / prediction / inference / new diagnostics occurred

Confirmed. No model was trained; nothing was scored; no prediction or inference was
generated; no new diagnostic was run.

## 23. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search occurred

Confirmed. None occurred.

## 24. Confirmation no namespace was created or mutated

Confirmed. No dataset or baseline namespace under `data/research/` or
`data/microstructure/` was created, read, hashed, refreshed, overwritten, deleted,
or otherwise mutated. The AH and AJ output namespaces were untouched.

## 25. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write occurred

Confirmed. None occurred and none is authorized.

## 26. Confirmation no data files were committed

Confirmed. The branch and this merge commit only the AK Markdown docs. No file under
`data/microstructure/` or `data/research/` is tracked or staged;
`.claude/scheduled_tasks.lock` is not committed.

## 27. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition occurred

Confirmed. No `research_eligible` flip; no `ml_authorized` /
`diagnostics_authorized` / strategy / backtest / live authorization transition; no
published manifest / gate report / sidecar / split file / research matrix / ML
config mutation. The Phase 4aw `flip_research_eligible(...)` always-raises invariant
was never invoked.

## 28. Validation commands and results from this merge review

- `git rev-parse --abbrev-ref HEAD` → `phase-4bn-ak/ml-arc-decision-memo`.
- `git rev-parse main` / `origin/main` → both `3e38fc87d148ed51ef23bfd76cf2f674a73fc8a0`.
- `git rev-parse phase-4bn-ak/ml-arc-decision-memo` → `608eca8abf49c9dcb546bde5439f79627aecf12f`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean; `git diff --check main..phase-4bn-ak/…` → clean.
- `git diff --name-status main..phase-4bn-ak/ml-arc-decision-memo` → two `A` docs
  files only (this closeout is added on the branch by the next commit):
  `2026-07-08_phase-4bn-ak_closeout.md`,
  `2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`.
- `git ls-tree -r --name-only phase-4bn-ak/ml-arc-decision-memo -- data/microstructure/`
  → empty.
- `git ls-tree -r --name-only phase-4bn-ak/ml-arc-decision-memo -- data/research/`
  → empty.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked each.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no source or test changed).

(These reflect the pre-merge review. Post-merge and post-finalization command
outputs are recorded in §31–§32 after the merge and in the final operator report.)

## 29. Git status before merge

`git status --short` on the branch shows only `?? .claude/scheduled_tasks.lock`
(untracked, not committed). No `data/` file staged or tracked.

## 30. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-ak/ml-arc-decision-memo` into `main`. No squash. No rebase. The
`.claude/scheduled_tasks.lock` transient and all data outputs are excluded.

## 31. Final merge commit SHA

`__PENDING_MERGE_COMMIT_SHA__` (finalized post-merge; see the finalization commit
and the final operator report).

## 32. Final main / origin main SHA

`__PENDING_FINAL_MAIN_SHA__` (finalized post-merge and post-push; see the final
operator report).

## 33. Result state

`ML_ARC_DECISION_MERGED_TO_MAIN__EXACTLY_ONE_BOUNDED_FOLLOWUP_SELECTED__FOLLOWUP_NOT_STARTED__NO_STRATEGY__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 34. Recommended state

**Remain paused.**

## 35. Explicit no-successor execution statement

No successor execution is authorized. The selected longer-horizon label memo, any
label build, any data generation, any data read, any ML, any diagnostics, any
strategy / signals / PnL / backtest / paper / shadow / live / exchange-write, and
any other successor phase require **separate future operator authorization**. This
merge records and integrates the arc decision only; it starts nothing.

## 36. Preserved project locks and verdicts

Preserved verbatim:

- locked cost **8 bps per side / 16 bps round-trip**;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked);
- Phase 4bb-F canonical `.sha256` sidecar policy;
- Phase 4bn-AE claim-scope and strategy / PnL / backtest / live hard boundary (§8 /
  §19);
- Phase 4bn-AH leakage/split-integrity proof and gitignored dataset-spec namespace
  posture (`test_rows_loaded = 0`; `v002_terminal_window_read = false`;
  `sealed_test_split_touched = false`);
- Phase 4bn-AI descriptive, no-model boundary;
- Phase 4bn-AJ fixed-baseline verdict (`CONTINUE_ONE_FOLLOWUP`) and no-strategy
  boundary;
- every earlier retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
  thread / V2 / G1 / C1) and project lock. Phase 4 canonical remains unauthorized.

## 37. Manifest / eligibility state preservation

- no `research_eligible` flip;
- no `ml_authorized` transition;
- no `diagnostics_authorized` transition;
- no strategy / backtest / live authorization transition;
- no published manifest / gate report / sidecar / split-file mutation.
