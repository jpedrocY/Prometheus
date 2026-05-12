# Phase 4bj-I — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-I — Chronological Split Policy Design Memo
- **Type:** docs-only design / governance memo
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bj-I from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bj-I records, at policy / design level only, the recommended
  chronological split policy for the locked label-family research
  cell (`microstructure_labels_aggtrades_v001` / BTCUSDT /
  2025-01-15). The memo's primary recommendation is **Option D** —
  declare the single-day cell insufficient for formal
  train / validation / test partitioning and **remain unsplit** until
  multi-day data exists; record the no-split determination as a
  sibling artefact under a separately authorized successor phase.
  The merge brings forward the Phase 4bj-I design memo, closeout,
  and a narrow `current-project-state.md` update. No data file is
  committed; no split artefact is created; no manifest is mutated;
  no successor phase is authorized.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-i/chronological-split-policy-design-memo`

## 2. SHAs

- **`main` SHA before merge:** `49d60b6e362294541b4f45f49c6e0b389b70b5b9`
  (Phase 4bj-H SHA-chain-fixup commit on top of the Phase 4bj-H
  merge-closeout `65e9094a46eb6423ac6132ea394a62a7e860c55d`).
- **Phase 4bj-I branch commit SHA:** `56d5203a4270f67e1153902e49dbe9d88d976b11`
  (`docs(phase-4bj-i): chronological split policy design memo`).
- **Merge commit SHA:** `8fc888fc64c2c00e497fda73ec2f55db8136216c`.
- **Merge-closeout commit SHA:** (recorded below once committed and pushed).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bj-I is the merge-closeout
  commit. Any one-commit SHA-chain-fixup on top of that anchor only
  records the final-`main` SHA value back into §2 of this
  merge-closeout; it does not change Phase 4bj-I lifecycle
  semantics, consistent with the Phase 4bb-G / Phase
  4bb-F-implementation / Phase 4bb-F / Phase 4bj-G / Phase 4bj-F /
  Phase 4bj-H SHA-chain-fixup precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bj-i/chronological-split-policy-design-memo`
- Strategy: `ort` (the default).
- Merge commit message:
  `docs(phase-4bj-i): merge chronological split policy design memo`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-i_chronological-split-policy-design-memo.md`
  (the 18-section Phase 4bj-I design memo)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-i_closeout.md`
  (the Phase 4bj-I closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bj-I narrative
  paragraph prepended above the Phase 4bj-H paragraph; new "Current
  phase:" Phase 4bj-I block; prior Phase 4bj-H "Current phase:"
  block preserved as historical context per the documented standard)

### Source / tests / scripts / config

- None.

### `data/microstructure/`

- **No `data/microstructure/` file was modified, created, moved,
  copied, renamed, or deleted by the merge.** All raw / derived /
  feature / label parquets, manifests, sidecars, gate reports, and
  successor-state artefacts remain byte-for-byte unchanged at their
  recorded historical paths and SHAs.

### Prior governance memos

- No prior governance memo was modified beyond the narrow
  `current-project-state.md` paragraph addition.

### Prior source / test / script

- No prior source, test, or script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 333 +++++++++++++
 ...4bj-i_chronological-split-policy-design-memo.md | 546 +++++++++++++++++++++
 .../2026-05-12_phase-4bj-i_closeout.md             | 149 ++++++
 3 files changed, 1028 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bj-I chronological split policy design memo +
Phase 4bj-I closeout + narrow `current-project-state.md` update. No
source / test / script / config / `data/microstructure/` files were
modified.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bj-I is project-complete after this merge and the
merge-closeout commit. The phase records — at policy / design level
only — the recommended chronological split policy for the locked
label-family research cell (`microstructure_labels_aggtrades_v001` /
BTCUSDT / 2025-01-15, 1,681,098 rows, 39 columns, four forward
horizons {1s, 5s, 15s, 60s}, 0 invalid-price rows, 676 censored rows
total). The memo's **primary recommendation is Option D** — declare
the single-day cell insufficient for formal
train / validation / test partitioning and remain unsplit until
multi-day data exists. Phase 4bj-I explicitly rejects Option B
(single-day train / validation / test vocabulary) as **unsafe**
because the vocabulary implies a generalisation guarantee the
single-day cell cannot support; it marks Option C (descriptive
within-day segmentation with neutral vocabulary) as
**conditional-only**, admissible solely under a separately
authorized successor phase that withholds ML / strategy / backtest
permission; and it locks down a uniform **60s purge / embargo
policy** as the default for any future within-day segmentation
(because 60s is the maximum forward horizon — purge / embargo width
must equal or exceed the worst-case label horizon to prevent
forward-leakage from train-to-test). The memo also predeclares the
sibling split-policy / split-artefact schema (a
`microstructure_labels_aggtrades_v001__v001__split_policy.json`
sibling under the gitignored `data/microstructure/successor-state/`
namespace, never a mutation of the original label manifest), defines
the label-evaluation gating sequence for any future Phase 4bj-K /
4bj-L-equivalent, lays out the conditional future phase ladder
(Phase 4bj-J split-artefact recording / 4bj-K label-diagnostic study
plan / 4bj-L label-diagnostic study execution / later ML / strategy /
backtest / paper / live phases), and re-integrates M0 / no-rescue
language (split partitions are not strategy regimes; labels are not
signals; retained failed strategy families remain closed; 5m thread
remains closed). The label manifest remains `research_eligible:
false`, `eligibility_gate_status: "pending"`, and
`chronological_split_policy: "not_yet_defined"`. All
`data/microstructure/` artefacts are byte-for-byte unchanged. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant was preserved (never invoked). No ML, label
evaluation, split-artefact creation, no-split determination
recording, label diagnostics, strategy, signal, backtest,
acquisition, paper / shadow, live-readiness, deployment,
exchange-write, production-key, authenticated-API, private-endpoint,
user-stream, MCP, Graphify, `.mcp.json`, or credential work was
authorized or performed. Recommended state remains **paused**.

## 7. Local gitignored outputs (if any)

**None.**

Phase 4bj-I is docs-only and produced no local artefact. The
previously recorded Phase 4bb-G raw successor-state JSON + sidecar,
the Phase 4bg-B / 4bi-D / 4bj-G derived / feature / label
successor-state artefacts, the Phase 4bb-D / 4bf / 4bi-B / 4bj-E
gate reports, and all raw / derived / normalized / feature / label
parquets, manifests, and sidecars remain at their recorded
gitignored paths and SHAs, untouched and unmodified.

## 8. Validation results

- `git diff --check` (post-merge): **clean** (no whitespace errors).
- `git status` (post-merge, pre-merge-closeout):
  ```text
  On branch main
  Your branch is ahead of 'origin/main' by 2 commits.
  Untracked files:
    .claude/scheduled_tasks.lock
    data/research/
  nothing added to commit but untracked files present
  ```
- `git check-ignore -v data/microstructure/`: `.gitignore:85:data/microstructure/	data/microstructure/`
  (boundary preserved; no `data/microstructure/` file affected by
  this merge).
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-I modifies no
  source code, no tests, no scripts, no `pyproject.toml`, no
  `README.md`, and no `.gitignore`. The latest authoritative
  whole-repo validation remains the Phase 4bb-F-implementation
  merge: `ruff check .` PASS, `mypy src/prometheus` (strict) Success
  on 120 source files, `pytest tests/research/microstructure/` 915
  passed + 1 skipped (pre-existing labelled placeholder), `pytest`
  (whole repo) 1698 passed + 1 skipped + 2 failed (the same
  pre-existing simulation `KeyError: 'trade_count'` failures in
  `tests/simulation/test_backtest_real_2026_03.py`; unchanged from
  prior phases; not introduced by this merge).

## 9. Upstream immutability evidence (if applicable)

Phase 4bj-I is a docs-only design / governance memo that does not
access any `data/microstructure/` artefact for read, computation, or
modification. Therefore no upstream artefact required active SHA
recomputation by Phase 4bj-I itself. The recorded SHAs from prior
phases remain authoritative and unchanged:

- raw manifest `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`
- raw zip `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- raw zip sidecar `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`
- acquisition log `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`
- Phase 4bb-D gate report `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`
- Phase 4bb-D gate report sidecar `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8`
- Phase 4bb-G raw successor-state `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`
- normalized parquet `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`
- original derived manifest `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
- Phase 4bf derived gate report `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`
- Phase 4bg-B derived successor-state `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`
- feature parquet `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
- feature manifest `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
- Phase 4bi-B feature gate report `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
- Phase 4bi-D feature successor-state `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
- label parquet `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26`
- label manifest `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3`
- Phase 4bj-E label gate report `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`
- Phase 4bj-G label successor-state `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5`

All artefacts byte-for-byte unchanged across the merge. The
Phase 4bb-D doubled-path gate report remains valid at its recorded
historical path; it was not migrated, copied, renamed, deleted, or
rewritten.

## 10. Manifest state preservation (if applicable)

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Governance labels |
| --- | --- | --- | --- | --- |
| Raw aggTrades (`microstructure_raw_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Derived normalized aggTrades (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Feature aggTrades (`microstructure_features_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Label aggTrades (`microstructure_labels_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | unchanged |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant **preserved (never invoked)** by Phase 4bj-I
or by the merge.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. Phase 4bj-I's primary recommendation (Option D)
explicitly preserves this `"not_yet_defined"` state: the
single-day cell is insufficient for formal partitioning and any
future no-split determination must be encoded as a **sibling
artefact** under the gitignored `data/microstructure/successor-state/`
namespace, never as a mutation of the original label manifest. The
secondary Option C (within-day descriptive segmentation with neutral
vocabulary) would likewise record its partition rule as a sibling
artefact, not as a manifest mutation, and only under a separately
authorized successor phase with ML / strategy / backtest permission
withheld.

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
  renamed, or deleted.
- No label parquet read for computation, modification, or
  recomputation.
- No train / validation / test split artefact created.
- No no-split determination artefact created.
- No within-day-segmentation artefact created.
- No sibling split-policy JSON created.
- No new manifest created.
- No new gate report created.
- No new successor-state artefact created.
- No raw / derived / feature / label eligibility gate rerun.
- No normalizer, kernel, or processing script run.
- No `research_eligible` flipped on any actual manifest.
- No `eligibility_gate_status` transitioned on any actual manifest.
- No `chronological_split_policy` changed on any actual manifest
  (the label manifest remains `"not_yet_defined"`).
- No ML model trained.
- No ML architecture designed.
- No feature ranked.
- No meta-labeling created.
- No label evaluated empirically.
- No label statistics computed beyond the documentation-level
  references already recorded in Phase 4bj-B / 4bj-C / 4bj-D /
  4bj-E / 4bj-G / 4bj-H.
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

The Phase 4bj-I merge does NOT, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels / features / OI / funding context /
  derivatives flow into trading signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- empirical label evaluation, label statistics computation,
  histogram / distribution / quantile / autocorrelation /
  cross-horizon-relationship analysis on the label parquet, or
  reading the label parquet for analysis (the memo only references
  already-recorded summary values);
- split artefact creation (no train / validation / test partitions
  on disk; no within-day segmentation artefacts; no sibling
  split-policy JSON; no no-split determination JSON);
- recording a no-split determination as a sibling artefact (the
  memo recommends Option D but does not create the sibling artefact;
  any such recording requires a separately authorized successor
  phase);
- mutating the label manifest's `chronological_split_policy` from
  `"not_yet_defined"` to any value (any future split policy must be
  recorded as a sibling artefact);
- transitioning any manifest's `research_eligible` from `false` to
  `true`;
- transitioning any manifest's `eligibility_gate_status` from
  `pending` to `pass` or `fail`;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation
  (existing horizons {1s, 5s, 15s, 60s} remain the only labels
  computed; no horizon extension is authorized);
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels (these label families remain out of scope);
- additional aggTrades / 5m / 1m / tick / mark-price / order-book /
  spot / cross-venue / funding / open-interest data acquisition;
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
- M0 amendment derived from Phase 4bj-I reasoning;
- broadening Phase 4bj-I design-memo language into binding
  cross-project governance beyond its docs-only scope;
- treating Option D (the primary recommendation) or Option C (the
  conditional secondary) as authorization to act — both options
  remain recommendations only and require separate operator
  authorization for any implementation.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

- Phase 4bj-J (or any equivalent Split Artefact Implementation /
  Recording — including the no-split-determination sibling artefact
  recording recommended by Option D)
- Phase 4bj-K (or any equivalent Label Diagnostic Study Plan)
- Phase 4bj-L (or any equivalent Label Diagnostic Study Execution)
- any future Phase 4bj-M / 4bj-N / 4bj-* successor in the labels
  arc
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

Phase 4bj-I is now project-complete on `main` after this merge and
the merge-closeout commit. The microstructure aggTrades lineage
arc remains in its post-Phase-4bj-H state with respect to artefacts:
every dataset family (raw / derived / feature / label) has a
machine-readable sibling successor-state marker recorded as a
gitignored JSON artefact, every original manifest remains
byte-identical with `research_eligible: false` and
`eligibility_gate_status: "pending"`, and the label manifest's
`chronological_split_policy` remains `"not_yet_defined"`. The
governance / design surface has been extended at policy level only:
the recommended chronological split policy is now on record (Option
D — single-day cell insufficient for formal
train / validation / test, remain unsplit until multi-day data
exists; record the no-split determination as a sibling artefact
under a separately authorized successor phase), the conditional
Option C path is on record (descriptive within-day segmentation with
neutral vocabulary; admissible only under a separately authorized
successor phase with ML / strategy / backtest permission withheld),
and the uniform 60s purge / embargo policy is on record as the
default for any future within-day segmentation. No successor phase
is authorized. Per the operator's instruction, the project remains
paused; any future phase requires a separately authorized prompt
that satisfies the Phase 4bk-A workflow standard, the Phase 4ak M0
twelve-clause gate, and the Phase 4al refined no-rescue rule.

**Conditional next, NOT authorized:** Phase 4bj-J-equivalent
**Split Artefact Recording** is the cleanest non-paused option. It
would be docs-and-local-gitignored-output only, would record the
Option D no-split determination as a sibling artefact under
`data/microstructure/successor-state/` (filename pattern
`microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json`)
plus paired `.sha256` sidecar, would not mutate the original label
manifest, would not create train / validation / test partitions on
disk, and would explicitly authorize none of: label diagnostics,
ML, strategy, signal construction, or backtests. Phase 4bj-J is
**not** authorised by this merge.
