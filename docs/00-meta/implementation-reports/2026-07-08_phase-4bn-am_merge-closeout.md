# Phase 4bn-AM — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AM — Longer-Horizon Label Contract / Spec Memo.
Branch: `phase-4bn-am/longer-horizon-label-contract-spec`.

## 2. Phase type

Docs-only longer-horizon label contract / specification memo; **merge-only review**.
No data read; no label built; no namespace created/mutated; no model; no rerun; no
source/test change; no successor execution authorized.

## 3. Base SHA

`4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`
(pre-AM `main` tip; the `docs(phase-4bn-al): finalize merge closeout shas` commit).

## 4. Pre-merge branch HEAD

`f01ee90ced4fc218fdd27be819d77bd98cd56e69`
(`docs(phase-4bn-am): record longer-horizon label contract spec`).

## 5. Main / origin main before merge

`main == origin/main == 4b96b671df485fffbe1f369baebcb8ecfdb4fe5e` (verified in sync
before merge).

## 6. Summary of the Phase 4bn-AM contract / spec memo

Phase 4bn-AM is the memo recommended by Phase 4bn-AL. It defines, at the design /
specification level only, a prospective longer-horizon aggTrades label layer. It
pre-registers: a **new sibling label family**
`microstructure_labels_longhorizon_aggtrades_v001` (the frozen v002 family cannot be
mutated — its horizon set is asserted `("1s","5s","15s","60s")`), reusing the v002
schema pattern; horizons **5m (300000 ms, lead) / 30m (1800000 ms) / 1h (3600000 ms)**;
per-horizon `forward_log_return_H` + `forward_direction_H` columns, per-horizon
`reference_row_index_H` / `reference_timestamp_ms_H` / `horizon_censored_flag_H`
support, global invalid/any-censored flags, the 17 lineage columns + `label_config_hash`;
a **strict-sign** direction policy (no deadband / no bp threshold / no optimization / no
cost-fitting), with cost-aware / magnitude / neutral-band options **evaluated but not
adopted**; a requirement that a future build report **descriptive** continuous-return
and 8 bps / 16 bps cost-clearing summaries per horizon × split; and the full leakage /
split / censoring, storage / budget, validation / proof-artefact, and interpretation /
claim-scope framework. It builds nothing, reads no data, creates no namespace, and
records a build recommendation.

## 7. Confirmation AM was docs-only

Confirmed. The Phase 4bn-AM branch adds exactly two Markdown files under
`docs/00-meta/implementation-reports/` (the contract/spec memo and its closeout) and
nothing else. No source / test / script / config / manifest / gate report / sidecar /
split file / ML config / research matrix / `data/` artefact was created or modified.

## 8. Confirmation current-project-state.md left unchanged and why

Confirmed unchanged. The update convention at this point is not clear/consistent: the
docs-only decision memos Phase 4bn-AE and 4bn-AG each added a paragraph, but the
subsequent Phase 4bn-AH / 4bn-AI / 4bn-AJ / 4bn-AK / 4bn-AL phases did not (the doc's
tracked tail still stops at Phase 3k / 2026-04-29), and the doc is flagged by the Phase
4bn-AE external review as an oversized/stale single-source-of-truth pending a
consolidation memo. Per the operator instruction and matching the immediate
AH/AI/AJ/AK/AL precedent, Phase 4bn-AM recorded the memo only in its report + closeout
and left `current-project-state.md` untouched (report §34).

## 9. Final AM decision

**`LABEL_CONTRACT_SPEC_RECORDED__LABEL_BUILD_AUTHORIZATION_RECOMMENDED`.**

## 10. Recommended future build

`microstructure_labels_longhorizon_aggtrades_v001` (a new sibling label family).

## 11. Recommended future build scope

- **Exactly one** future **label-build authorization phase**.
- **Admitted pre-v002 aggTrades segment only** (2024-03-01..2024-11-30; 275
  partitions; the AH-verified feature/normalized/raw sources).
- **New sibling family**, not a mutation of the frozen v002 family.
- Horizons **5m / 30m / 1h**; **5m lead**; **30m and 1h secondary diagnostic**.
- **Strict-sign extension** for `forward_direction_H`.
- **No cost-aware / magnitude / deadband label adopted by default** (any future use
  must be fixed, pre-registered, cost-locked, separately authorized).
- **Compact label Parquet + sidecars + inventory + manifest + leakage/split/censoring
  proof.**
- **Descriptive continuous-return and 8 bps / 16 bps cost-clearing summaries** per
  horizon × split (+ per-month / per-date where feasible).
- **Preserve AH leakage invariants** (completed-event target; past-only features;
  strict alignment; chrono split + 1-day boundary embargo; per-horizon earlier-split
  boundary crossings = 0; per-horizon envelope-terminal censoring with the censored
  fraction measured and growing with H).
- **Preserve the AH compact-spec posture.**
- **Preserve the Phase 4bn-L 125 GiB derived cap**; **budget preflight required** in
  the future build.
- **Local / gitignored namespace only.**
- **All non-authorization flags `false`.**
- **v002 terminal excluded**; **sealed test excluded**; **`test_rows_loaded = 0`
  preserved**.
- **ML / diagnostics / strategy excluded** (evaluating the built labels is a further,
  separate authorization).

## 12. Confirmation the recommended future build is not started

Confirmed. No build work has begun; no prompt for the build was generated.

## 13. Confirmation the recommended future build requires separate future operator authorization

Confirmed. The recommended label-build phase begins only under a separate future
operator prompt, and the build may read data only under that prompt.

## 14. Confirmation any data read / build requires separate future authorization

Confirmed. No data read or build is authorized by this memo or this merge; both require
a separate future operator prompt and full pre-registration compliance.

## 15. Summary of why label-build authorization was recommended

- A **safe, precise contract is definable from committed evidence** (schema pattern,
  alignment keys, chrono split + 1-day embargo, per-horizon censoring, cost lock all
  recovered from committed source) — so `LABEL_CONTRACT_SPEC_BLOCKED` did not apply.
- The **frozen v002 label family covers only 1s / 5s / 15s / 60s**.
- **5m / 30m / 1h require a new sibling family.**
- The **open economic-materiality question** (do longer-horizon raw moves clear the
  16 bps cost materially more often?) **requires a bounded descriptive build to
  measure**.
- **No-build would dead-end the longer-horizon line without a safety justification**
  (the build is bounded, descriptive, over already-admitted data, all
  non-authorization flags false).
- The **recommendation is not an authorization** — the build still needs its own
  separate operator prompt.

## 16. Preserved allowed claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_ALLOWED`):

- **short-horizon directional information exists** about `forward_direction_15s` on the
  pre-v002 segment;
- the **v002 small-lift directional sign is reproduced** on the larger, earlier
  pre-v002 regime;
- the **calibration / confidence tail beats the majority floor on accuracy but is
  overconfident in level** — ranking/diagnostic use only, not calibrated probabilities.

No new empirical claim was added; longer-horizon content is design-level and
qualitative; no empirical longer-horizon distribution was invented.

## 17. Preserved forbidden claims

Preserved verbatim (Phase 4bn-AE §8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing may be
cited as evidence of: **tradability; profitability; strategy viability; execution
viability; slippage/spread adequacy; live-readiness; paper/shadow readiness; PnL;
backtest validity; production suitability; economic significance.** The memo does not
claim longer horizons are tradable. The 2.47%-of-moves-clear-cost figure is descriptive
context, not evidence of edge. Locked cost remains **8 bps per side / 16 bps
round-trip**.

## 18. Confirmation no data files were read during AM or the merge review

Confirmed. No feature/label Parquet, no v002 terminal window, no sealed test, no raw
zip, no AH/AJ local result artefact, no endpoint — during Phase 4bn-AM or this merge
review. Only `git status` / `git ls-files` / `git ls-tree` / `git check-ignore`
tracked-state checks were run against `data/` paths.

## 19. Confirmation no longer-horizon label was built or generated

Confirmed. No longer-horizon label, label column, label Parquet, sidecar, manifest, or
proof artefact was built or generated.

## 20. Confirmation no label / dataset / output namespace was created or mutated

Confirmed. No new label / dataset / baseline / research / output namespace was created;
the AH and AJ namespaces were not inspected, hashed, refreshed, mutated, overwritten, or
deleted.

## 21. Confirmation no source / test / manifest / gate / sidecar / split / ML-config change occurred

Confirmed. No source module, test, script, published manifest, gate report, sidecar,
split file, or ML config was created or modified.

## 22. Confirmation no AH builder rerun occurred

Confirmed. The Phase 4bn-AH data-reading dataset builder was not re-run; its one-run
guard and output namespace were untouched.

## 23. Confirmation no AI diagnostics rerun occurred

Confirmed. The Phase 4bn-AI descriptive diagnostics were not re-run.

## 24. Confirmation no AJ baseline rerun occurred

Confirmed. The Phase 4bn-AJ fixed baseline runner (`majority` / `persistence` / `L2`)
was not re-run.

## 25. Confirmation no AJ/AI/AH metrics were revised, recomputed, or re-derived

Confirmed. Every figure was quoted verbatim from the committed AH / AI / AJ / AK / AL
reports; nothing was recomputed, revised, or re-derived.

## 26. Confirmation no model / scoring / prediction / inference / new diagnostics occurred

Confirmed. No model was trained, scored, or evaluated; no prediction or inference was
produced; no new diagnostic was run.

## 27. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search occurred

Confirmed. None occurred.

## 28. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write occurred

Confirmed. None occurred.

## 29. Confirmation no data files were committed

Confirmed. No file under `data/microstructure/` or `data/research/` (or anywhere under
`data/`) was staged or committed; `.claude/scheduled_tasks.lock` was not committed.

## 30. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition occurred

Confirmed. No `research_eligible` flip; no `ml_authorized` / `diagnostics_authorized` /
strategy / backtest / live authorization transition; no published manifest / gate
report / sidecar / split file mutation. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant was preserved and never invoked.

## 31. Validation commands and results from this merge review

- `git rev-parse --abbrev-ref HEAD` → `phase-4bn-am/longer-horizon-label-contract-spec`.
- `git rev-parse main` / `origin/main` → both
  `4b96b671df485fffbe1f369baebcb8ecfdb4fe5e`.
- `git rev-parse phase-4bn-am/longer-horizon-label-contract-spec` →
  `f01ee90ced4fc218fdd27be819d77bd98cd56e69`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean.
- `git diff --name-status main..phase-4bn-am/longer-horizon-label-contract-spec` → two
  added docs (`..._longer-horizon-label-contract-spec.md`, `..._closeout.md`); no
  modifications.
- `git ls-tree -r --name-only phase-4bn-am/... -- data/microstructure/` → empty.
- `git ls-tree -r --name-only phase-4bn-am/... -- data/research/` → empty.
- `git ls-files data/microstructure/` → 0 tracked. `git ls-files data/research/` → 0
  tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `.claude/scheduled_tasks.lock` → not staged, not committed.
- No pytest / ruff / mypy required (docs-only; no code surface changed).

(These reflect the pre-merge review; the merge-closeout commit adds this third docs
file. Post-merge and post-finalization command outputs are reproduced in the final
operator report.)

## 32. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked; no `data/` file staged; branch tip
`f01ee90ced4fc218fdd27be819d77bd98cd56e69` (+ the merge-closeout commit added on the
branch before merge).

## 33. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-am/longer-horizon-label-contract-spec` into `main`. No squash; no rebase; no
`.claude/scheduled_tasks.lock`; no data outputs.

## 34. Final merge commit SHA

`0c89f51a267e6ea8aec77ad01f252c74332ad4c5`
(`docs(phase-4bn-am): merge longer-horizon label contract spec`; `--no-ff`, 3 docs
files added: the memo, its closeout, and this merge-closeout).

## 35. Final main / origin main SHA

Equal to this SHA-finalization commit (`docs(phase-4bn-am): finalize merge closeout
shas`), which is the resulting `main` / `origin/main` tip after push; the literal value
is reproduced in the final operator report (a commit cannot embed its own SHA).

## 36. Result state

`LONGER_HORIZON_LABEL_CONTRACT_SPEC_MERGED_TO_MAIN__LABEL_BUILD_AUTHORIZATION_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 37. Recommended state

**Remain paused.**

## 38. Explicit no-successor execution statement

The recommended longer-horizon label-build phase, any label build, any data generation,
any data read, any ML, any diagnostics, any strategy / signals / PnL / backtest / paper
/ shadow / live-readiness / exchange-write, and any other successor phase require
**separate future operator authorization**. Phase 4bn-AM and this merge authorize **no**
successor execution phase and do **not** generate the recommended build prompt.

## 39. Preserved project locks and verdicts

Preserved verbatim:

- **8 bps per side / 16 bps round-trip** locked cost (§11.6).
- **Phase 4aw `flip_research_eligible(...)` always-raises invariant** (never invoked).
- **Phase 4bb-F canonical sidecar policy.**
- **Phase 4bn-AE claim-scope and strategy/PnL/backtest/live boundary** (§8 / §19).
- **Phase 4bn-AH proof and dataset namespace posture** (leakage/split proof;
  `test_rows_loaded = 0`; compact-spec; no v002 terminal / sealed test).
- **Phase 4bn-AI descriptive no-model boundary.**
- **Phase 4bn-AJ fixed baseline verdict and no-strategy boundary**
  (`CONTINUE_ONE_FOLLOWUP`; information-diagnostic, non-economic).
- **Phase 4bn-AK single-follow-up selection** (`longer_horizon_label_memo`; other three
  deferred).
- **Phase 4bn-AL label-memo recommendation and no-build / no-data-read boundary.**
- **Phase 4bn-AM label-contract / spec recommendation and no-build / no-data-read
  boundary.**
- Plus the retained strategy-research locks (H0 / R3 / R1a / R1b-narrow / R2 / F1 /
  D1-A / 5m thread / V2 / G1 / C1) and the Phase 4ak M0 twelve-clause gate / Phase 4al
  no-rescue constraints. Phase 4 canonical remains unauthorized.

## 40. Manifest / eligibility state preservation

- No `research_eligible` flip.
- No `ml_authorized` transition.
- No `diagnostics_authorized` transition.
- No strategy / backtest / live authorization transition.
- No published manifest / gate report / sidecar / split file mutation.
