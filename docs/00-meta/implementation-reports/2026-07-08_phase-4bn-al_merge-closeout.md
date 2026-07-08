# Phase 4bn-AL — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AL — Longer-Horizon Label Memo.
Branch: `phase-4bn-al/longer-horizon-label-memo`.

## 2. Phase type

Docs-only longer-horizon label memo; **merge-only review**. No data read; no label
built; no namespace; no model; no rerun; no successor execution authorized.

## 3. Base SHA

`205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`
(pre-AL `main` tip; the `docs(phase-4bn-ak): finalize merge closeout shas` commit).

## 4. Pre-merge branch HEAD

`2b257f7e06ba98c8535ddb7a861c5c5689ac4432`
(`docs(phase-4bn-al): record longer-horizon label memo`).

## 5. Main / origin main before merge

`main == origin/main == 205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f` (verified in sync
before merge).

## 6. Summary of the Phase 4bn-AL memo

Phase 4bn-AL is the selected Phase 4bn-AK bounded follow-up
(`longer_horizon_label_memo`, Phase 4bn-AE §16(a)). It is a **docs-only design memo**
evaluating whether a future longer-horizon (5m / 30m / 1h) label design is a
reasonable next research contract. It recovered the AK / AJ / AI / AH evidence and the
AE claim/cost/dependence framework from committed reports and committed source
constants; stated the 15s-label problem (real short-horizon directional information
but economically thin — only 2.47% of validation 15s moves clear the locked 16 bps
round-trip cost; median move 2.53 bps); gave the rationale for longer horizons (larger
raw moves, more economically interpretable, less bounce-sensitive) alongside their
risks (feature signal decay beyond microstructure memory, regime drift, heavy overlap /
effective-sample collapse, growing censoring near segment ends); evaluated six
candidate label families; analysed 5m / 30m / 1h separately; specified the
leakage/split/censoring, storage/budget/build, mid-price-deferred, and
strategy/PnL/backtest/live implications; and recorded a decision. It confirmed the
existing label family (`microstructure_labels_aggtrades_v001`) covers only 1s/5s/15s/60s,
so 5m/30m/1h is a **new label layer**.

## 7. Confirmation AL was docs-only

Confirmed. The Phase 4bn-AL branch adds exactly two Markdown files under
`docs/00-meta/implementation-reports/` (the memo and its closeout) and nothing else.
No source / test / script / config / manifest / gate report / sidecar / split file /
ML config / research matrix / `data/` artefact was created or modified.

## 8. Confirmation current-project-state.md left unchanged and why

Confirmed unchanged. The update convention at this point is not clear/consistent: the
docs-only decision memos Phase 4bn-AE and 4bn-AG each added a paragraph, but the
subsequent Phase 4bn-AH / 4bn-AI / 4bn-AJ / 4bn-AK phases did not (the doc's tracked
tail still stops at Phase 3k / 2026-04-29), and the doc is flagged by the Phase 4bn-AE
external review as an oversized/stale single-source-of-truth pending a consolidation
memo. Per the operator instruction and matching the immediate AH/AI/AJ/AK precedent,
Phase 4bn-AL recorded the memo only in its report + closeout and left
`current-project-state.md` untouched (report §29).

## 9. Final AL decision

**`RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`.**

## 10. Recommended next memo

Exactly one next **docs-only** phase: a **longer-horizon label contract / spec memo**.

## 11. Recommended next memo scope

- Docs-only **design + pre-registration only** (no build, no data read, no namespace).
- Horizons **5m / 30m / 1h at design level**.
- **5m primary / lead**; **30m and 1h secondary diagnostic**.
- **Conservative multi-horizon diagnostic family** default.
- **Strict-sign extension** to the new horizons **plus continuous forward-return
  distribution reporting**.
- **Descriptive 8 bps / 16 bps cost-clearing share reporting** (economic materiality
  as a diagnostic, not a baked-in target; cost-aware / magnitude / deadband options
  evaluated but not adopted-by-default, and only ever under a fixed, pre-registered,
  never-optimized threshold tied to the locked 16 bps).
- **Censoring / embargo / storage / leakage / claim-scope pre-registration**.

## 12. Confirmation the recommended next memo is not started

Confirmed. No work on the recommended memo has begun; no prompt for it was generated.

## 13. Confirmation the recommended next memo requires separate future operator authorization

Confirmed. The recommended longer-horizon label contract / spec memo begins only under
a separate future operator prompt; selecting/recommending it consumes the single Phase
4bn-AK follow-up budget.

## 14. Confirmation any actual label build / data generation / data read requires further separate authorization

Confirmed. Even the recommended memo is docs-only; any actual longer-horizon label
build, data generation, or data read requires its **own further** separate operator
authorization beyond that memo (with a budget preflight and preservation of the AH
compact-spec posture and the Phase 4bn-L 125 GiB cap).

## 15. Summary of why the label contract / spec memo was recommended

- Phase 4bn-AJ showed **real short-horizon directional information** (L2 +5.03 pp over
  majority / +2.96 pp over persistence; validation date- and month-block agreement
  1.000; no holdout sign reversal).
- The **single binding limitation is economic thinness at 15s**.
- Only **2.47%** of validation 15s moves clear the locked **16 bps** round-trip cost
  (median move 2.53 bps).
- The **existing label family covers only 1s / 5s / 15s / 60s**.
- **5m / 30m / 1h are a new label layer.**
- A **docs-only spec memo is the safest next design step** — it commits no data /
  build / strategy, forces the design to be made deliberately and pre-registered, and
  defers the unmeasured empirical question to a later separately-authorized build.
  Closing would be premature (the signal-decay risk is unmeasured); insufficient-
  evidence does not apply (the design-level recommendation is fully decidable now).

## 16. Preserved allowed claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_ALLOWED`):

- **short-horizon directional information exists** about `forward_direction_15s` on
  the pre-v002 segment;
- the **v002 small-lift directional sign is reproduced** on the larger, earlier
  pre-v002 regime;
- the **calibration / confidence tail beats the majority floor on accuracy but is
  overconfident in level** — usable for ranking/diagnostic reading only, not as
  calibrated probabilities.

No new empirical claim was added; longer-horizon reasoning is design-level and
qualitative; no empirical longer-horizon distribution was invented.

## 17. Preserved forbidden claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing may be
cited as evidence of: **tradability; profitability; strategy viability; execution
viability; slippage/spread adequacy; live-readiness; paper/shadow readiness; PnL;
backtest validity; production suitability; economic significance.** The
2.47%-of-moves-clear-cost figure is descriptive context, not evidence of edge.
`forward_direction_15s` remains an information-diagnostic, non-economic target that may
embed bid-ask bounce (aggTrades-only, no mid/book). The memo does **not** claim longer
horizons will be tradable. Locked cost remains **8 bps per side / 16 bps round-trip**.

## 18. Confirmation no data files were read during AL or the merge review

Confirmed. No feature/label Parquet, no v002 terminal window, no sealed test, no raw
zip, no AH/AJ local result artefact, no endpoint — during Phase 4bn-AL or this merge
review. Only `git status` / `git ls-files` / `git ls-tree` / `git check-ignore`
tracked-state checks were run against `data/` paths.

## 19. Confirmation no longer-horizon label was built or generated

Confirmed. No longer-horizon label, label column, or label layer was built, generated,
or written.

## 20. Confirmation no label / dataset namespace was created or mutated

Confirmed. No new label / dataset / baseline / research namespace was created; the AH
and AJ namespaces were not inspected, hashed, refreshed, mutated, overwritten, or
deleted.

## 21. Confirmation no AH builder rerun occurred

Confirmed. The Phase 4bn-AH data-reading dataset builder was not re-run; its one-run
guard and output namespace were untouched.

## 22. Confirmation no AI diagnostics rerun occurred

Confirmed. The Phase 4bn-AI descriptive diagnostics were not re-run.

## 23. Confirmation no AJ baseline rerun occurred

Confirmed. The Phase 4bn-AJ fixed baseline runner (`majority` / `persistence` / `L2`)
was not re-run.

## 24. Confirmation no AJ/AI/AH metrics were revised, recomputed, or re-derived

Confirmed. Every figure was quoted verbatim from the committed AH / AI / AJ / AK
reports; nothing was recomputed, revised, or re-derived.

## 25. Confirmation no model / scoring / prediction / inference / new diagnostics occurred

Confirmed. No model was trained, scored, or evaluated; no prediction or inference was
produced; no new diagnostic was run.

## 26. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search occurred

Confirmed. None occurred.

## 27. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write occurred

Confirmed. None occurred.

## 28. Confirmation no data files were committed

Confirmed. No file under `data/microstructure/` or `data/research/` (or anywhere under
`data/`) was staged or committed; `.claude/scheduled_tasks.lock` was not committed.

## 29. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition occurred

Confirmed. No `research_eligible` flip; no `ml_authorized` / `diagnostics_authorized`
/ strategy / backtest / live authorization transition; no published manifest / gate
report / sidecar / split file mutation. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant was preserved and never invoked.

## 30. Validation commands and results from this merge review

- `git rev-parse --abbrev-ref HEAD` → `phase-4bn-al/longer-horizon-label-memo`.
- `git rev-parse main` / `origin/main` → both
  `205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`.
- `git rev-parse phase-4bn-al/longer-horizon-label-memo` →
  `2b257f7e06ba98c8535ddb7a861c5c5689ac4432`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean.
- `git diff --name-status main..phase-4bn-al/longer-horizon-label-memo` → two added
  docs (`..._longer-horizon-label-memo.md`, `..._closeout.md`); no modifications.
- `git ls-tree -r --name-only phase-4bn-al/longer-horizon-label-memo -- data/microstructure/`
  → empty.
- `git ls-tree -r --name-only phase-4bn-al/longer-horizon-label-memo -- data/research/`
  → empty.
- `git ls-files data/microstructure/` → 0 tracked. `git ls-files data/research/` → 0
  tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no code surface changed).

(These reflect the pre-merge review; the merge-closeout commit adds this third docs
file. Post-merge and post-finalization command outputs are reproduced in the final
operator report.)

## 31. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked; no `data/` file staged; branch tip
`2b257f7e06ba98c8535ddb7a861c5c5689ac4432` (+ the merge-closeout commit added on the
branch before merge).

## 32. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-al/longer-horizon-label-memo` into `main`. No squash; no rebase; no
`.claude/scheduled_tasks.lock`; no data outputs.

## 33. Final merge commit SHA

`67267ac20ff97060a38652652a2733c42d7d375b`
(`docs(phase-4bn-al): merge longer-horizon label memo`; `--no-ff`, 3 docs files added:
the memo, its closeout, and this merge-closeout).

## 34. Final main / origin main SHA

Equal to this SHA-finalization commit (`docs(phase-4bn-al): finalize merge closeout
shas`), which is the resulting `main` / `origin/main` tip after push; the literal
value is reproduced in the final operator report (a commit cannot embed its own SHA).

## 35. Result state

`LONGER_HORIZON_LABEL_MEMO_MERGED_TO_MAIN__LABEL_CONTRACT_MEMO_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 36. Recommended state

**Remain paused.**

## 37. Explicit no-successor execution statement

The recommended longer-horizon label contract / spec memo, any label build, any data
generation, any data read, any ML, any diagnostics, any strategy / signals / PnL /
backtest / paper / shadow / live-readiness / exchange-write, and any other successor
phase require **separate future operator authorization**. Phase 4bn-AL and this merge
authorize **no** successor execution phase and do **not** generate the recommended
next memo's prompt.

## 38. Preserved project locks and verdicts

Preserved verbatim:

- **8 bps per side / 16 bps round-trip** locked cost (§11.6).
- **Phase 4aw `flip_research_eligible(...)` always-raises invariant** (never invoked).
- **Phase 4bb-F canonical sidecar policy.**
- **Phase 4bn-AE claim-scope and strategy/PnL/backtest/live boundary** (§8/§19).
- **Phase 4bn-AH proof and dataset namespace posture** (leakage/split proof;
  `test_rows_loaded = 0`; compact-spec; no v002 terminal / sealed test).
- **Phase 4bn-AI descriptive no-model boundary.**
- **Phase 4bn-AJ fixed baseline verdict and no-strategy boundary**
  (`CONTINUE_ONE_FOLLOWUP`; information-diagnostic, non-economic).
- **Phase 4bn-AK single-follow-up selection** (`longer_horizon_label_memo`; other
  three deferred).
- **Phase 4bn-AL label-memo recommendation and no-build / no-data-read boundary.**
- Plus the retained strategy-research locks (H0 / R3 / R1a / R1b-narrow / R2 / F1 /
  D1-A / 5m thread / V2 / G1 / C1) and the Phase 4ak M0 twelve-clause gate / Phase 4al
  no-rescue constraints. Phase 4 canonical remains unauthorized.

## 39. Manifest / eligibility state preservation

- No `research_eligible` flip.
- No `ml_authorized` transition.
- No `diagnostics_authorized` transition.
- No strategy / backtest / live authorization transition.
- No published manifest / gate report / sidecar / split file mutation.
