# Phase 4bj-K — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-K — Label Diagnostic Study Plan
- **Type:** docs-only design / governance memo
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bj-K from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bj-K authored a docs-only predeclared diagnostic study
  plan for any future Phase 4bj-L-equivalent label diagnostic
  execution phase against the locked one-day BTCUSDT 2025-01-15
  cell (`microstructure_labels_aggtrades_v001`). It defines in
  advance the allowed descriptive diagnostics, the forbidden
  diagnostics and outputs, the per-horizon exclusion / censoring
  rules, the no-split / no-segmentation execution mode, the
  optional future neutral-segmentation gate, the leakage checks,
  the future output-path and JSON-schema conventions, the 13 stop
  conditions, the interpretation limits, the future phase ladder,
  and the M0 / no-rescue integration. The plan is not execution.
  The merge brings forward the Phase 4bj-K implementation report,
  closeout, and narrow `current-project-state.md` update. No data
  file is committed; no manifest is mutated; no successor phase is
  authorized.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-k/label-diagnostic-study-plan`

## 2. SHAs

- **`main` SHA before merge:** `13dac8ffb611ec14a728f99f98f85dd47ccda76c`
  (Phase 4bj-J SHA-chain-fixup commit on top of the Phase 4bj-J
  merge-closeout `5e5fc401d0776c7e86a4e0e0677cce87789b67b5`).
- **Phase 4bj-K branch commit SHA:** `8d72bf058404784a9cf47406384a812c774551cb`
  (`docs(phase-4bj-k): label diagnostic study plan`).
- **Merge commit SHA:** `64f6a76d6d8aafd71238fc22bf0f53c33c7feffa`.
- **Merge-closeout commit SHA:** `0074f696d5f4e9bd7fccf665d6742c77af2edaa2`
  (`docs(phase-4bj-k): add merge closeout`).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bj-K is the merge-closeout
  commit `0074f696d5f4e9bd7fccf665d6742c77af2edaa2`. This
  one-commit SHA-chain-fixup on top of that anchor only records the
  final-`main` SHA value back into §2 of this merge-closeout; it
  does not change Phase 4bj-K lifecycle semantics, consistent with
  the Phase 4bb-G / Phase 4bb-F-implementation / Phase 4bb-F /
  Phase 4bj-G / Phase 4bj-F / Phase 4bj-H / Phase 4bj-I / Phase
  4bj-J SHA-chain-fixup precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bj-k/label-diagnostic-study-plan`
- Strategy: `ort` (the default).
- Merge commit message:
  `docs(phase-4bj-k): merge label diagnostic study plan`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-k_label-diagnostic-study-plan.md`
  (the Phase 4bj-K main memo)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-k_closeout.md`
  (the Phase 4bj-K closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bj-K narrative
  paragraph prepended above the Phase 4bj-J paragraph; new "Current
  phase:" Phase 4bj-K block; prior Phase 4bj-J "Current phase:"
  block preserved as historical context per the documented
  standard)

### Source / tests / scripts / config

- None.

### `data/microstructure/`

- **No `data/microstructure/` file was modified, created, moved,
  copied, renamed, or deleted by the merge.** All raw / derived /
  feature / label parquets, manifests, sidecars, gate reports, and
  successor-state artefacts (including the Phase 4bj-J no-split
  determination JSON and its paired `.sha256` sidecar) remain
  byte-for-byte unchanged at their recorded paths and SHAs. Phase
  4bj-K is docs-only; it produces no local artefact under
  `data/microstructure/`.

### Prior governance memos

- No prior governance memo was modified beyond the narrow
  `current-project-state.md` paragraph addition.

### Prior source / test / script

- No prior source, test, or script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 456 ++++++++++++++
 .../2026-05-12_phase-4bj-k_closeout.md             |  80 +++
 ...5-12_phase-4bj-k_label-diagnostic-study-plan.md | 655 +++++++++++++++++++++
 3 files changed, 1191 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bj-K main memo + Phase 4bj-K closeout +
narrow `current-project-state.md` update. No source / test /
script / config / `data/microstructure/` files were modified.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bj-K is project-complete after this merge and the
merge-closeout commit. The phase records a docs-only predeclared
diagnostic study plan for any future Phase 4bj-L-equivalent label
diagnostic execution phase. The plan:

- enumerates 15 allowed future diagnostic categories (label schema
  / column-presence confirmation; row-count / row-order
  confirmation; per-horizon non-null / censored / valid count
  table; per-horizon forward return descriptive statistics;
  per-horizon direction class balance; per-horizon zero / flat-rate
  review; censoring location review; right-edge row review;
  timestamp monotonicity and uniqueness checks; feature-label
  row-index alignment check; feature-label timestamp alignment
  check; horizon-overlap leakage audit; documentation-only
  comparison against manifest summary values; conditional
  descriptive within-cell temporal stability check; conditional
  naive descriptive baselines);
- enumerates the complete forbidden-diagnostic and forbidden-output
  list (train / validation / test diagnostics; model fitting /
  scoring / selection; feature ranking / importance; label-to-
  signal conversion; threshold / hyperparameter search; strategy
  rules; entry / exit logic; PnL / MFE / MAE / R-multiple / equity
  / position simulation; alpha / edge claims; backtests; paper /
  shadow / live-readiness claims; acquisition recommendations
  based only on diagnostics; any result that reopens R2 / F1 /
  D1-A / V2 / G1 / C1 / 5m thread);
- locks the per-horizon exclusion and censoring rules to
  `horizons = ["1s", "5s", "15s", "60s"]` with
  `censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`
  and `invalid_price_row_count = 0`;
- locks the default no-split / no-segmentation execution mode (no
  train / validation / test; no within-day segmentation unless
  separately authorized; every output flagged
  `single_day_descriptive_diagnostics_only=true` and
  `no_generalization_interpretation=true`);
- defines an optional future neutral-segmentation gate (separate
  authorization required; neutral vocabulary only; uniform 60s
  purge / embargo; boundary-overlap masks; segmentation artefact
  as sibling gitignored JSON; no ML / strategy / backtest
  permission; no segment treated as holdout / validation / test);
- enumerates the 10 required leakage checks;
- defines the future output artefact plan (suggested future root
  `data/microstructure/diagnostics/labels/`; suggested future
  report filename pattern
  `microstructure_labels_aggtrades_v001__v001__label_diagnostics__phase-4bj-l.json`;
  paired `.sha256` sidecar in canonical Phase 4bb-F format;
  gitignored output only; deterministic JSON);
- defines a future 35+ key diagnostic result schema;
- enumerates 13 stop conditions for any future execution;
- records the interpretation limits (descriptive characterization
  of the locked single-day cell only; possible recommendation for
  multi-day data requirements; possible recommendation to remain
  paused; possible recommendation for a future failure-
  interpretation memo; cannot support ML feasibility / strategy
  hypothesis / backtest authorization / acquisition authorization
  / edge / alpha / predictive validity / live-readiness);
- enumerates decision options A–F (A remain paused, no plan; **B
  docs-only plan, no execution — selected**; C future Phase 4bj-L
  on full single-day cell; D future neutral segmentation memo
  before diagnostics; E future multi-day acquisition requirements;
  **F ML / strategy / backtest now — FORBIDDEN**);
- records the future phase ladder (Phase 4bj-L → multi-day aggTrades
  expansion requirements memo → acquisition authorization memo →
  multi-day acquisition execution → normalization / feature /
  label regeneration arcs for multi-day data → split policy design
  for multi-day data → split artefact recording for multi-day data
  → label diagnostics on multi-day data → ML feasibility memo →
  baseline ML diagnostic → failure-interpretation / fallback
  selection memo → strategy hypothesis under M0 → strategy spec →
  backtest plan → backtest execution → paper / shadow / live only
  much later under separate authorization), all marked NOT
  authorized by Phase 4bj-K;
- records the M0 / no-rescue integration (diagnostics are upstream
  of ML feasibility; ML diagnostics are upstream of M0 strategy
  admission; diagnostics do not bypass M0; labels are not signals;
  no-split determination is not an edge claim; one-day diagnostics
  are not generalisation evidence; retained failed strategy
  families remain closed; 5m thread remains operationally closed).

Phase 4bj-K does **not** run diagnostics, compute label statistics,
create diagnostic outputs, create train / validation / test splits,
create within-day segmentation artefacts, create split artefacts,
modify the label parquet, modify the label manifest, modify any
sidecar, mutate `chronological_split_policy`, mutate
`research_eligible`, mutate `eligibility_gate_status`, train ML,
design ML architecture, rank features, create meta-labeling,
create a strategy, run backtests, acquire data, call any endpoint,
open any WebSocket, use any credential, enable MCP or Graphify,
revise any retained verdict, change any project lock, amend M0,
merge anything else, commit anything under `data/microstructure/`,
or authorize Phase 4bj-L / any Phase 4bj-M / 4bj-N / 4bj-*
successor / Phase 5 / Phase 4 canonical / paper / shadow /
live-readiness / deployment / exchange-write / production keys /
authenticated APIs / private endpoints / user stream / live
WebSocket implementation.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. The Phase 4bj-J Option D no-split
determination remains encoded ONLY in the Phase 4bj-J sibling
JSON at the gitignored path
`data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json`;
Phase 4bj-K does not write to that artefact, does not duplicate
it, and does not broaden its scope. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant was preserved (never invoked). Recommended state remains
**paused**.

## 7. Local gitignored outputs (if any)

**None.**

Phase 4bj-K is docs-only and produced no local artefact under
`data/microstructure/`. The Phase 4bj-J no-split determination JSON
and its paired `.sha256` sidecar remain at their recorded
gitignored paths (SHA256
`7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`
for the JSON and
`9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8`
for the sidecar), byte-identical pre/post-merge. They remain local
gitignored output only; the merge does not touch them.

## 8. Validation results

- `git diff --check` (post-merge): **clean** (no whitespace errors).
- `git status` (post-merge, pre-merge-closeout):

  ```text
  On branch main
  Your branch is ahead of 'origin/main' by 1 commits.
  Untracked files:
    .claude/scheduled_tasks.lock
    data/research/
  nothing added to commit but untracked files present
  ```

- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-K modifies
  no source code, no tests, no scripts, no `pyproject.toml`, no
  `README.md`, and no `.gitignore`. The latest authoritative
  whole-repo validation remains the Phase 4bb-F-implementation
  merge: `ruff check .` PASS, `mypy src/prometheus` (strict)
  Success on 120 source files, `pytest tests/research/microstructure/`
  915 passed + 1 skipped (pre-existing labelled placeholder),
  `pytest` (whole repo) 1698 passed + 1 skipped + 2 failed (the
  same pre-existing simulation `KeyError: 'trade_count'` failures
  in `tests/simulation/test_backtest_real_2026_03.py`; unchanged
  from prior phases; not introduced by this merge).

## 9. Upstream immutability evidence (if applicable)

For every prior `data/microstructure/` artefact, pre-merge vs
post-merge SHA256 is IDENTICAL:

| Artefact | SHA256 |
| --- | --- |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Raw zip sidecar | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| Acquisition log | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bb-D raw gate report sidecar | `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8` |
| Phase 4bb-G raw successor-state | `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Phase 4bf derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B derived successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Phase 4bi-B feature gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Phase 4bi-D feature successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| Label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` |
| Label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` |
| Phase 4bj-E label gate report | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| Phase 4bj-G label successor-state | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |
| Phase 4bj-J no-split determination JSON | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` |
| Phase 4bj-J no-split determination sidecar | `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8` |

All twenty-three prior artefacts byte-for-byte unchanged across the
merge. Phase 4bj-K produces no new local artefact under
`data/microstructure/`. The Phase 4bb-D doubled-path gate report
remains valid at its recorded historical path; it was not migrated,
copied, renamed, deleted, or rewritten.

## 10. Manifest state preservation (if applicable)

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Governance labels |
| --- | --- | --- | --- | --- |
| Raw aggTrades (`microstructure_raw_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Derived normalized aggTrades (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Feature aggTrades (`microstructure_features_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Label aggTrades (`microstructure_labels_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | unchanged |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant **preserved (never invoked)** by Phase
4bj-K or by the merge.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. Phase 4bj-K explicitly **does not** mutate
this field on the original manifest. The Phase 4bj-J Option D
no-split determination remains encoded ONLY in the Phase 4bj-J
sibling JSON; Phase 4bj-K plans diagnostics that would run against
that determination but does not run them, mutate it, or broaden
it.

## 11. Boundary confirmations

- No source code modified.
- No test modified.
- No script modified.
- No `pyproject.toml` modified.
- No `README.md` modified.
- No `.gitignore` modified.
- No MCP file modified.
- No prior governance memo modified (beyond the narrow
  `current-project-state.md` paragraph addition + Current-phase
  block update).
- No `data/microstructure/` file modified, created, moved, copied,
  renamed, or deleted by the merge.
- No `data/microstructure/` file committed.
- The Phase 4bj-J no-split determination JSON and paired `.sha256`
  sidecar (local gitignored only) remain at their recorded paths
  and SHAs; the merge does not rewrite, move, copy, rename, or
  modify either file.
- No label parquet read for computation, modification, or
  recomputation.
- No label statistics computed.
- No diagnostic outputs created.
- No train / validation / test split artefact created.
- No within-day descriptive segmentation artefact created.
- No additional successor-state artefact created.
- No new manifest created.
- No new gate report created.
- No raw / derived / feature / label eligibility gate rerun.
- No normalizer, kernel, or processing script run.
- No `research_eligible` flipped on any actual manifest.
- No `eligibility_gate_status` transitioned on any actual manifest.
- No `chronological_split_policy` changed on any actual manifest
  (label manifest remains `"not_yet_defined"`).
- No ML model trained.
- No ML architecture designed.
- No feature ranked.
- No meta-labeling created.
- No label evaluated empirically.
- No strategy created.
- No signal computed.
- No backtest run.
- No PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output computed.
- No data acquired.
- No order-book data acquired.
- No mark-price data acquired.
- No spot / cross-venue data acquired.
- No funding / open-interest data acquired.
- No additional aggTrades data acquired.
- No public endpoint called.
- No Binance API called.
- No authenticated API called.
- No private endpoint called.
- No user stream used.
- No WebSocket opened.
- No credential created or read.
- No `.env` created or modified.
- No `.mcp.json` created or read.
- No MCP enabled.
- No Graphify enabled.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No successor phase authorized.

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 13. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant
- Phase 4bb-F canonical path policy (raw → `gate-reports/raw/`,
  normalized → `gate-reports/normalized/`, features →
  `gate-reports/features/`, labels → `gate-reports/labels/`,
  successor-state → flat under `successor-state/`)

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bj-K merge does NOT, and cannot, be construed as
authorising:

- empirical label evaluation, label statistics computation,
  histogram / distribution / quantile / autocorrelation /
  cross-horizon-relationship analysis on the label parquet, or
  any reading of the label parquet for analysis (Phase 4bj-K is
  text-only; the label parquet is referenced only at the
  documentation-level summary already recorded in prior phases);
- diagnostic artefact creation (no diagnostic JSON / CSV / parquet
  / sidecar; no diagnostic gate report; no diagnostic successor-
  state artefact);
- train / validation / test partition creation (the cell remains
  unsplit per Phase 4bj-J Option D);
- within-day descriptive segmentation artefact creation;
- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels / features / OI /
  funding context / derivatives flow into trading signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- mutating the label manifest's `chronological_split_policy` from
  `"not_yet_defined"` to any value;
- transitioning any manifest's `research_eligible` from `false` to
  `true`;
- transitioning any manifest's `eligibility_gate_status` from
  `pending` to `pass` or `fail`;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- Phase 4 canonical or Phase 5 authorisation;
- Phase 4bj-L (label diagnostic study execution), or any Phase
  4bj-M / 4bj-N / 4bj-* successor in the labels arc;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades / 5m / 1m / tick / funding / open-interest data
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening
  (R2 cost-fragility, F1 catastrophic floor, D1-A mechanism /
  framework mismatch, V2 design-stage incompatibility, G1
  regime-gate sparseness, C1 fires-and-loses anti-validation —
  all remain terminal for their first specs);
- 5m research-thread reopening (Phase 3t closure preserved);
- any rescue of R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread;
- creation of R3-prime / R1a-prime / R1b-narrow-prime / R2-prime /
  H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension /
  G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid /
  V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bj-K reasoning;
- broadening Phase 4bj-K study-plan language into binding
  cross-project governance beyond its docs-only scope.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

- Phase 4bj-L (or any equivalent Label Diagnostic Study Execution)
- any future Phase 4bj-M / 4bj-N / 4bj-* successor in the labels
  arc
- any future multi-day aggTrades expansion requirements memo
- any future acquisition authorization memo
- any future multi-day acquisition execution
- any future normalization / feature / label regeneration arc for
  multi-day data
- any future split policy design for multi-day data
- any future split artefact recording for multi-day data
- any future label diagnostics on multi-day data
- any future ML feasibility memo
- any future baseline ML diagnostic
- any future failure-interpretation / fallback-selection memo
- any future strategy hypothesis memo under M0
- any future strategy spec memo
- any future backtest plan memo
- any future backtest execution phase
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book /
  spot / cross-venue / funding / open-interest data acquisition
- ML implementation, ML training, model selection, feature
  ranking, meta-labeling
- strategy implementation, signal computation, backtest
  implementation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- public-endpoint calls in code
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials

## 16. Recommended state

**Remain paused.**

Phase 4bj-K is now project-complete on `main` after this merge and
the merge-closeout commit. The microstructure aggTrades lineage
arc remains in its post-Phase-4bj-J state with respect to
artefacts: every dataset family (raw / derived / feature / label)
has a machine-readable sibling successor-state marker recorded as
a gitignored JSON artefact under
`data/microstructure/successor-state/`, every original manifest
remains byte-identical with `research_eligible: false` and
`eligibility_gate_status: "pending"`, the label manifest's
`chronological_split_policy` remains `"not_yet_defined"`, and the
Phase 4bj-J Option D no-split determination remains encoded ONLY
in the Phase 4bj-J sibling JSON. Phase 4bj-K adds no artefact; it
adds a docs-only study plan defining what any future Phase 4bj-L-
equivalent diagnostic execution would be allowed to do, what it
would be forbidden to do, and what the predeclared output
conventions would be. The plan is governance, not edge evidence.
Labels remain not signals. No successor phase is authorized. Per
the operator's instruction, the project remains paused; any
future phase requires a separately authorized prompt that
satisfies the Phase 4bk-A workflow standard, the Phase 4ak M0
twelve-clause gate, and the Phase 4al refined no-rescue rule.

**Conditional next, NOT authorized:** Two distinct future
strategic options remain on the menu, both of which Phase 4bj-K
explicitly does **not** authorize:

1. **Phase 4bj-L-equivalent — Label Diagnostic Study Execution**
   (docs-and-code; low-stakes; descriptive only; no ML / strategy
   / backtest). This would execute the Phase 4bj-K-locked
   diagnostics against the locked single-day BTCUSDT 2025-01-15
   cell only, with explicit single-day-only / no-generalization
   flagging on every output and explicit non-authorization of any
   further successor. It would NOT authorize Phase 5, paper /
   shadow, live-readiness, deployment, exchange-write, ML,
   strategy, or backtest.

2. **Multi-day aggTrades expansion requirements memo** (docs-only).
   This would predeclare the requirements for acquiring multi-day
   aggTrades data (symbols, days, integrity governance, manifest
   structure, governance labels, expected use). This is the more
   meaningful research path because it is the only one that can
   eventually support generalisation-style partitioning, but it
   is also the one that costs more downstream phases. It would
   NOT authorize Phase 5, paper / shadow, live-readiness,
   deployment, exchange-write, ML, strategy, backtest, or any
   data acquisition (it would predeclare the requirements only;
   acquisition itself would be a later separately authorized
   phase).

Neither is authorized by this merge. The next strategic choice is
an operator decision and requires a separately authorized
authorization prompt per the Phase 4bk-A workflow standard.
