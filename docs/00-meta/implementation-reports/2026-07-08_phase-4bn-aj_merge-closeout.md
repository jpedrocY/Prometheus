# Phase 4bn-AJ — Merge Closeout

## 1. Phase name and branch

- **Phase:** 4bn-AJ — Fixed Pre-v002 Baseline Run + Verdict.
- **Source branch:** `phase-4bn-aj/fixed-pre-v002-baseline-run-verdict`.
- **Target branch:** `main`.
- **Action:** merge into `main`.

## 2. Phase type

Code + controlled pre-v002 baseline read/run + local gitignored compact results;
**merge-only review** here (no baseline rerun, no data read during the merge).

## 3. Base SHA

`f33831c8577764c5fbc059a9e23ab4f13f0c8ed2`
(`docs(phase-4bn-ai): finalize merge closeout shas`).

## 4. Pre-merge branch HEAD

`2e90970a8b6e7842dc2123ebf667fef533225598`
(`docs(phase-4bn-aj): add fixed baseline verdict closeout`). Branch commits:

- `f3c827f` — `code(phase-4bn-aj): implement fixed pre-v002 baseline runner`
  (source + tests).
- `2e90970` — `docs(phase-4bn-aj): add fixed baseline verdict closeout`
  (implementation report + closeout).

## 5. Main / origin main before merge

`main == origin/main == f33831c8577764c5fbc059a9e23ab4f13f0c8ed2` (verified in
sync before the merge).

## 6. Summary of Phase 4bn-AJ implementation

`pre_v002_fixed_baseline_run.py` re-verifies the four Phase 4bn-AH dataset-spec
artefacts + all 550 pre-v002 feature/label Parquet sidecars via the reused Phase
4bn-AH read path, runs a real Phase 4bn-L budget preflight, **applies** the
AH-fitted `train_only_transform.json` statistics (refits nothing), and makes two
streaming, bounded-memory passes — a fit pass (L2 SGD on the 214 train dates +
re-derived train class counts, cross-checked against the AH manifest) and an eval
pass (majority / persistence / L2 predictions accumulated per family × split ×
UTC-month × UTC-date, plus L2 calibration bins and a `forward_log_return_15s` cost
histogram). It excludes the two embargo dates, drops invalid/censored/null rows
exactly as AH did (never imputes a target), fits only on `train`, and writes nine
compact JSON artefacts + Phase 4bb-F sidecars to the single gitignored AJ namespace
(no model binaries, no row-level predictions). The three Phase 4bn-B pure-numpy
baseline implementations and the AF/AH modules were **imported and reused**, not
edited.

## 7. Summary of Phase 4bn-AJ fixed baseline run

Single controlled run, **~47.0 min (2,822.8 s)**. 275/275 partitions verified;
**304,816,127** train rows fit **once**; **396,930,283** rows evaluated **once**
(both equal the AH kept totals exactly). Each baseline ran exactly once; the
one-run guard refuses overwrite. `test_rows_loaded = 0`;
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`; 0 embargo
rows used.

## 8. Baselines

- **majority** — modal train class (= **+1 up**);
- **persistence** — `sign(rolling_log_return_past_window_15s)` (matched to 15s);
- **L2 linear** — multinomial-logistic softmax regression, frozen Phase 4bn-B SGD
  constants (1 epoch, batch 8192, lr 0.1, L2 1e-4, grad-clip 10, seed 20260528).

## 9. Key validation result (this merge review)

- `pytest` AJ + AF + AH (offline) → **146 passed** (23 AJ + 97 AF + 26 AH), no
  regression; these tests do **not** rerun the AH builder or the AJ baseline runner.
- `ruff check` (AJ module + test) → **All checks passed**.
- `mypy` (AJ module) → **0 direct errors**; residual errors surface only from
  imported v002 sibling modules (`ml_baseline_models_v002` / `_metrics_v002`) and
  the AH module under `strict=true` (bare-`np.ndarray` convention) — **pre-existing,
  unmodified by this phase**.
- `git diff --check` → clean.
- `git diff --name-status main..branch` → 4 added files (2 docs, 1 source, 1 test);
  no data, no manifest/gate/sidecar/split/ML-config, no model binaries, no
  row-level predictions.
- `git ls-tree -r branch -- data/microstructure/` → 0; `… -- data/research/` → 0.
- `git ls-files …/ml_datasets/pre_v002_contract_v001/` → 0;
  `… …/ml_baselines/pre_v002_fixed_baseline_v001/` → 0.
- `git check-ignore` → `data/microstructure/` `.gitignore:85`; `data/research/`
  and both output namespaces `.gitignore:88`.
- Read-only re-hash → AH namespace **4/4 byte-identical** (manifest `36a13213…`,
  transform `85f6ea35…`, split `d1681acd…`, proof `e36c9163…`); AJ namespace 9
  artefacts + 9 sidecars verify.

## 10. Key metric summary (15s, validation split)

- majority accuracy **0.4950**; persistence accuracy **0.5158**; L2 accuracy
  **0.5453**;
- L2 accuracy uplift over majority **+5.03 pp**; over persistence **+2.96 pp**;
- L2 macro-F1 **0.3660** (majority floor 0.2207 → uplift **+0.145**); L2 balanced
  accuracy 0.3689 (uplift +3.56 pp over majority);
- L2 high-confidence tail (≥ 0.8) accuracy **0.633** vs majority floor 0.495 —
  beats the floor on all splits (though overconfident in level);
- validation date- and month-block agreement **1.000**; holdout does not reverse
  the sign (holdout L2 +4.1 pp over majority); no overfitting (validation−train
  accuracy +0.008);
- validation 15s moves exceeding the 16 bps round-trip cost **2.47%** —
  **descriptive only**, not a tradability/economic claim.

## 11. Verdict

**`CONTINUE_ONE_FOLLOWUP`** (Phase 4bn-AE §16; `kill_reasons = []`). Reproduces the
v002 small-lift sign (+5.03 pp accuracy / +0.145 macro-F1 over majority) on the
larger, earlier pre-v002 regime, with full block stability and — unlike v002 — a
high-confidence tail that beats the floor.

## 12. Caveat

Persistence macro-F1 (0.402) exceeds L2 macro-F1 (0.366) **solely** because
persistence predicts the degenerate ~1.5% flat class (a tick-structure artifact per
§9); on the two directional classes L2 dominates, and the +0.03 macro-F1 threshold
is majority-floor-referenced (matching the §16 "+0.14 macro-F1" v002 anchor). Under
a stricter "macro-F1 over both floors" reading the verdict would be
`INVESTIGATE_AMBIGUOUS`; **both readings converge on the same action** — a
separately-authorized Phase 4bn-AK arc-decision, default **remain paused**, no
successor here.

## 13. No baseline rerun during merge

Confirmed. The Phase 4bn-AJ baseline runner was **not** invoked during this merge
review. Validation used only the offline synthetic test suite + git state checks +
read-only hash recompute.

## 14. No AH builder rerun

Confirmed. The Phase 4bn-AH builder was not re-invoked; its one-run guard remains
active.

## 15. No AH namespace mutation

Confirmed. `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
remains 4 artefacts + 4 sidecars, all four SHA256 byte-identical to the AH/AI/AJ
values. Nothing created, overwritten, deleted, mutated, or refreshed.

## 16. No AJ namespace mutation during merge

Confirmed. `data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001/`
remains 9 artefacts + 9 sidecars, all verifying. The merge review only read it.

## 17. No feature/label Parquet row read during merge

Confirmed. No Parquet row was read during the merge review (the row-level read
occurred only in the Phase 4bn-AJ run itself, already recorded).

## 18. No v002 terminal read, no sealed test touch, test_rows_loaded = 0 preserved

Confirmed as recorded in the AH/AJ proofs and re-verified read-only:
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`.

## 19. No unregistered models / model selection / hyperparameter search / feature selection / threshold optimization

Confirmed. Exactly the three pre-registered baselines (frozen constants) were run,
once each; none of these occurred during the phase or the merge review.

## 20. No strategy/signals/PnL/backtest/paper/shadow/live/exchange-write

Confirmed. None occurred. No Sharpe / trading hit-rate / position sizing /
execution logic.

## 21. No data files committed

Confirmed. The branch tracks 0 files under `data/microstructure/` and 0 under
`data/research/`. The merge brings forward only source, tests, and docs.

## 22. AH and AJ output namespaces remain local, gitignored, uncommitted

Confirmed. Both under `data/research/` (`.gitignore:88`); `git ls-files` → 0 tracked
for each. Local and uncommitted.

## 23. Validation commands and results (this merge review)

As §9. All PASS; post-check `git status --short` shows only the expected transient
untracked `.claude/scheduled_tasks.lock`.

## 24. Git status before merge

```text
?? .claude/scheduled_tasks.lock
```

## 25. Merge method

`git checkout main` → confirm `main == f33831c` → `git merge --no-ff
phase-4bn-aj/fixed-pre-v002-baseline-run-verdict -m "code(phase-4bn-aj): merge
fixed pre-v002 baseline run verdict"`. `ort` strategy; no squash; no rebase; no
`--no-verify`; no `--no-gpg-sign`; no force-push. `.claude/scheduled_tasks.lock`
and all data outputs excluded. Then push to `origin/main`.

## 26. Final merge commit SHA

`11ece8ef15ff310ac98d6e27f35422cee76ac692`
(`code(phase-4bn-aj): merge fixed pre-v002 baseline run verdict`).

## 27. Final main / origin main SHA

Equal to this SHA-finalization commit (`docs(phase-4bn-aj): finalize merge closeout
shas`), which is the resulting `main` / `origin/main` tip after push; reproduced in
the final operator report and `git log`. Post-merge `git status --short` shows only
`.claude/scheduled_tasks.lock`; `git ls-files` for both output namespaces returns 0
tracked files (both gitignored, `.gitignore:88`); both namespaces remain
byte-identical.

## 28. Result state

`FIXED_PRE_V002_BASELINE_RUN_MERGED_TO_MAIN__PRE_REGISTERED_VERDICT_PRESERVED__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 29. Recommended state

**Remain paused.**

## 30. Explicit no-successor authorization

**None.** No successor is authorized by this merge. Phase 4bn-AK (arc-decision), any
§16 (a)–(d) follow-up, ML training, model scoring, predictions, inference, strategy,
signals, PnL, backtests, additional data reads, an AH builder rerun, an AJ baseline
rerun, a new dataset namespace, a new baseline namespace, v003, compacted Parquet,
database outputs, paper/shadow, live-readiness, deployment, exchange-write,
credentials, private/authenticated endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, and all other candidates each require **separate operator
authorization**.

## 31. Preserved project locks and verdicts

All preserved verbatim: §11.6 = 8 bps per side / 16 bps round-trip; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical path + sidecar policy; Phase 4bn-AH proof and namespace posture; Phase
4bn-AI descriptive no-model boundary; Phase 4bn-AE claim-scope and strategy
boundary (§8/§19). All prior phase results (Phase 4bn-Z … AI) preserved.

## 32. Manifest / eligibility state preservation

No `research_eligible` flip; no `ml_authorized` transition; no
`diagnostics_authorized` transition; no strategy/backtest/live authorization
transition; no published manifest / gate report / sidecar / split file mutation.
The AJ run read the published feature/label Parquet **read-only** and wrote only a
separate local gitignored compact result namespace.
