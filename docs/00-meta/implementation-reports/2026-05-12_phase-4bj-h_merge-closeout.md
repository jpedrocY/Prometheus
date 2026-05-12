# Phase 4bj-H — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-H — Label Evaluation / Chronological Split Boundary Memo
- **Type:** docs-only boundary / governance memo
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bj-H from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bj-H records the policy boundary between the completed
  microstructure artefact-governance arc (raw / derived / feature /
  label families) and any future empirical label study. The merge
  brings forward the Phase 4bj-H boundary memo, closeout, and narrow
  `current-project-state.md` update. No data file is committed; no
  empirical label evaluation was performed; no split artefact was
  created; no successor phase is authorized.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-h/label-evaluation-chronological-split-boundary-memo`

## 2. SHAs

- **`main` SHA before merge:** `1064d2932ed34bc706a2311139a5431e788ce798`
  (Phase 4bb-G SHA-chain-fixup commit on top of the Phase 4bb-G
  merge-closeout `3f52176889fdb6ce91b227b2140002e7f44aba6b`).
- **Phase 4bj-H branch commit SHA:** `2b723caa5a0a786242d4f6b343ac7bdc07ce1553`
  (`docs(phase-4bj-h): label evaluation / chronological split
  boundary memo`).
- **Merge commit SHA:** `c085a50c86a8e87c8a72f09f7e10b6c0f889c12a`.
- **Merge-closeout commit SHA:** (recorded below once committed and
  pushed; a one-commit SHA-chain-fixup will follow to record the
  final-`main` SHA back into §2 of this merge-closeout, consistent
  with Phase 4bb-G / Phase 4bb-F-implementation / Phase 4bb-F /
  Phase 4bj-G / Phase 4bj-F SHA-chain-fixup precedents).
- **Final `main` / `origin/main` SHA after push:** (recorded below
  once the merge-closeout commit + SHA-chain-fixup are pushed).

## 3. Merge method

- Command: `git merge --no-ff phase-4bj-h/label-evaluation-chronological-split-boundary-memo`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bj-h): merge label evaluation /
  chronological split boundary memo`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-h_label-evaluation-chronological-split-boundary-memo.md`
  (the 16-section Phase 4bj-H boundary memo)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-h_closeout.md`
  (the 12-section Phase 4bj-H closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bj-H narrative
  paragraph prepended above the Phase 4bb-G paragraph; new "Current
  phase:" Phase 4bj-H block; prior Phase 4bb-G "Current phase:"
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
 docs/00-meta/current-project-state.md              | 306 +++++++++++++++
 .../2026-05-12_phase-4bj-h_closeout.md             | 147 +++++++
 ...evaluation-chronological-split-boundary-memo.md | 432 +++++++++++++++++++++
 3 files changed, 885 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bj-H boundary memo + Phase 4bj-H closeout +
narrow `current-project-state.md` update. No source / test / script
/ config / `data/microstructure/` files were modified.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bj-H is project-complete after this merge and the
merge-closeout commit. The phase records — at policy level only —
the boundary between the completed microstructure artefact-governance
arc and any future empirical label study. Specifically, Phase 4bj-H
defines what "label evaluation" means in this project (a future
controlled diagnostic activity, never a strategy or signal),
declares the chronological split boundary rule (no empirical label
evaluation may run before a chronological split policy is recorded
as a sibling artefact, never as a mutation of the original label
manifest), enumerates a ten-item leakage risk register, locks down
the input-family boundary (current governed family is aggTrades-
derived; order-book / mark-price / spot / cross-venue / candle /
funding / OI / additional aggTrades families remain out of scope),
records fallback-lane framing at policy level only, and lays out a
safe future phase ladder (Phase 4bj-I / 4bj-J / 4bj-K / 4bj-L and
later ML / strategy / backtest / paper / live phases) all of which
are explicitly **NOT authorized** by this merge. The label manifest
remains `research_eligible: false`, `eligibility_gate_status:
"pending"`, and `chronological_split_policy: "not_yet_defined"`. All
`data/microstructure/` artefacts are byte-for-byte unchanged. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant was preserved (never invoked). No ML, label
evaluation, strategy, signal, backtest, acquisition, paper / shadow,
live-readiness, deployment, exchange-write, production-key,
authenticated-API, private-endpoint, user-stream, MCP, Graphify,
`.mcp.json`, or credential work was authorized or performed.
Recommended state remains **paused**.

## 7. Local gitignored outputs (if any)

**None.**

Phase 4bj-H is docs-only and produced no local artefact. The
previously recorded Phase 4bb-G raw successor-state JSON + sidecar,
and the prior Phase 4bg-B / 4bi-D / 4bj-G successor-state artefacts,
remain at their recorded gitignored paths and SHAs, untouched and
unmodified.

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
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-H modifies no
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

Phase 4bj-H is a docs-only boundary memo that does not access any
`data/microstructure/` artefact for read, computation, or
modification. Therefore no upstream artefact required active SHA
recomputation by Phase 4bj-H itself. The recorded SHAs from prior
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
always-raises invariant **preserved (never invoked)** by Phase 4bj-H
or by the merge.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. Phase 4bj-H explicitly records that any future
chronological split policy must be encoded as a **sibling artefact**
under a gitignored namespace, never as a mutation of the original
label manifest.

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
- No new manifest created.
- No new gate report created.
- No new successor-state artefact created.
- No raw / derived / feature / label eligibility gate rerun.
- No normalizer, kernel, or processing script run.
- No `research_eligible` flipped on any actual manifest.
- No `eligibility_gate_status` transitioned on any actual manifest.
- No `chronological_split_policy` changed on any actual manifest.
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

The Phase 4bj-H merge does NOT, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels / features / OI / funding context /
  derivatives flow into trading signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- empirical label evaluation, label statistics computation, or
  reading the label parquet for analysis (the boundary memo only
  references already-recorded summary values);
- chronological split artefact creation or recording;
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
- M0 amendment derived from Phase 4bj-H reasoning;
- broadening Phase 4bj-H boundary-memo language into binding
  cross-project governance beyond its docs-only scope.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

- Phase 4bj-I (or any equivalent Chronological Split Policy Design
  Memo)
- Phase 4bj-J (or any equivalent Split Artefact Implementation /
  Recording)
- Phase 4bj-K (or any equivalent Label Diagnostic Study Plan)
- Phase 4bj-L (or any equivalent Label Diagnostic Study Execution)
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

Phase 4bj-H is now project-complete on `main` after this merge and
the merge-closeout commit. The microstructure aggTrades lineage
arc remains in its post-Phase-4bb-G state: every dataset family
(raw / derived / feature / label) has a machine-readable sibling
successor-state marker recorded as a gitignored JSON artefact, every
original manifest remains byte-identical with `research_eligible:
false` and `eligibility_gate_status: "pending"`, the label
manifest's `chronological_split_policy` remains `"not_yet_defined"`,
and the boundary between artefact governance and any future
empirical label study is now documented at policy level. No
successor phase is authorized. Per the operator's instruction, the
project remains paused; any future phase requires a separately
authorized prompt that satisfies the Phase 4bk-A workflow standard,
the Phase 4ak M0 twelve-clause gate, and the Phase 4al refined
no-rescue rule.

**Conditional next, NOT authorized:** Phase 4bj-I-equivalent
**Chronological Split Policy Design Memo** is the cleanest
non-paused option. It would be docs-only and would record partition
rules for the locked BTCUSDT 2025-01-15 cell (or record the
determination that the cell cannot be partitioned), enumerate
embargo / purge requirements for overlapping horizons, define the
recommended sibling-artefact recording approach, and explicitly
authorize none of: split artefact creation, label diagnostics, ML,
strategy, or backtests. Phase 4bj-I is **not** authorised by this
merge.
