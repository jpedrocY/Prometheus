# Phase 4bj-J — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-J — No-Split Determination Recording
- **Type:** docs + local gitignored sibling artefact recording
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bj-J from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bj-J operationalizes the Phase 4bj-I Option D policy
  decision (single-day cell insufficient for formal train /
  validation / test partitioning; remain unsplit until multi-day
  data exists) into exactly one machine-readable sibling no-split
  determination JSON artefact for the label family
  `microstructure_labels_aggtrades_v001` / BTCUSDT / 2025-01-15,
  plus exactly one paired SHA256 sidecar, under the canonical
  Phase 4bb-F `data/microstructure/successor-state/` namespace.
  The merge brings forward the Phase 4bj-J implementation report,
  closeout, and narrow `current-project-state.md` update. No data
  file is committed; no manifest is mutated; no successor phase is
  authorized. The no-split determination JSON and its paired
  `.sha256` sidecar remain local gitignored output only.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-j/no-split-determination-recording`

## 2. SHAs

- **`main` SHA before merge:** `dd11b2d39e0179bca040485aa1c876741b5fa32b`
  (Phase 4bj-I SHA-chain-fixup commit on top of the Phase 4bj-I
  merge-closeout `8f920e00fc3e0f2064baac6d723eb75c61e81044`).
- **Phase 4bj-J branch commit SHA:** `d8969abf1553ad4f369666057edf6b87c749078a`
  (`docs(phase-4bj-j): no-split determination recording`).
- **Merge commit SHA:** `a9edfc0edfa0db55b51f66d653d00f735a3231d7`.
- **Merge-closeout commit SHA:** (recorded below once committed and pushed).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bj-J is the merge-closeout
  commit. Any one-commit SHA-chain-fixup on top of that anchor only
  records the final-`main` SHA value back into §2 of this
  merge-closeout; it does not change Phase 4bj-J lifecycle
  semantics, consistent with the Phase 4bb-G / Phase
  4bb-F-implementation / Phase 4bb-F / Phase 4bj-G / Phase 4bj-F /
  Phase 4bj-H / Phase 4bj-I SHA-chain-fixup precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bj-j/no-split-determination-recording`
- Strategy: `ort` (the default).
- Merge commit message:
  `docs(phase-4bj-j): merge no-split determination recording`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-j_no-split-determination-recording.md`
  (the Phase 4bj-J implementation report)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-j_closeout.md`
  (the Phase 4bj-J closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bj-J narrative
  paragraph prepended above the Phase 4bj-I paragraph; new "Current
  phase:" Phase 4bj-J block; prior Phase 4bj-I "Current phase:"
  block preserved as historical context per the documented
  standard)

### Source / tests / scripts / config

- None.

### `data/microstructure/`

- **No `data/microstructure/` file was modified, created, moved,
  copied, renamed, or deleted by the merge.** All raw / derived /
  feature / label parquets, manifests, sidecars, gate reports, and
  successor-state artefacts (including the Phase 4bj-J no-split
  determination JSON and its paired `.sha256` sidecar created on
  the branch) remain byte-for-byte unchanged at their recorded
  paths and SHAs. The Phase 4bj-J no-split determination JSON and
  sidecar are **local gitignored output only**; they were not
  staged or committed by the branch, and the merge introduces
  nothing new under `data/microstructure/`.

### Prior governance memos

- No prior governance memo was modified beyond the narrow
  `current-project-state.md` paragraph addition.

### Prior source / test / script

- No prior source, test, or script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 428 +++++++++++++++++++++
 .../2026-05-12_phase-4bj-j_closeout.md             |  76 ++++
 ...phase-4bj-j_no-split-determination-recording.md | 377 ++++++++++++++++++
 3 files changed, 881 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bj-J implementation report + Phase 4bj-J
closeout + narrow `current-project-state.md` update. No source /
test / script / config / `data/microstructure/` files were
modified.

## 6. Verdict

**LOCAL ARTEFACT PRODUCED.**

Phase 4bj-J is project-complete after this merge and the
merge-closeout commit. The phase encoded the Phase 4bj-I Option D
policy decision into exactly one machine-readable sibling no-split
determination JSON artefact at
`data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json`
(14,236 bytes; SHA256
`7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`),
with exactly one paired `.sha256` sidecar at the same path + `.sha256`
suffix (141 bytes; canonical Phase 4bb-F two-space `<sha>  <basename>\n`
body; SHA256
`9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8`).
Both files are local gitignored output only and are NOT committed;
the merge does not contain any `data/microstructure/` write. The
single-day BTCUSDT 2025-01-15 label cell (1,681,098 rows; 39
columns; horizons {1s, 5s, 15s, 60s};
`censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`;
`invalid_price_row_count = 0`;
`label_config_hash = fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`)
is declared insufficient for formal train / validation / test
partitioning, and the cell remains unsplit until multi-day data
exists. No train / validation / test partitions exist on disk. No
within-day descriptive segmentation artefacts exist on disk. The
terms `train` / `validation` / `test` remain forbidden for the
single-day cell; future descriptive segmentation (if ever
authorized) must use neutral vocabulary (`fixture-A` /
`fixture-B` / `fixture-C` / `early-day` / `mid-day` / `late-day`)
and remain descriptive-only with a uniform 60s purge / embargo
policy. The no-split determination is encoded ONLY in the new
sibling JSON; the original label manifest's
`chronological_split_policy` remains `"not_yet_defined"`. All
`data/microstructure/` artefacts are byte-for-byte unchanged. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant was preserved (never invoked). No label
diagnostics were run. No label statistics were computed beyond the
documentation-level summary values already recorded in Phase 4bj-B
/ 4bj-C / 4bj-D / 4bj-E / 4bj-G / 4bj-H / 4bj-I. No empirical
label evaluation has been run. No ML training, ML architecture,
feature ranking, meta-labeling, strategy, signal, backtest,
acquisition, paper / shadow, live-readiness, deployment,
exchange-write, production-key, authenticated-API, private-endpoint,
user-stream, MCP, Graphify, `.mcp.json`, or credential work was
authorized or performed. Recommended state remains **paused**.

## 7. Local gitignored outputs (if any)

The Phase 4bj-J no-split determination artefact and its paired
sidecar were produced on the branch as local gitignored output
only; both are still present at their recorded paths and SHA256
digests after the merge:

| Artefact | Path | SHA256 | Size | Committed? |
| --- | --- | --- | --- | --- |
| No-split determination JSON | `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json` | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` | 14,236 bytes | NO |
| Paired `.sha256` sidecar | same path + `.sha256` suffix | `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8` | 141 bytes | NO |

Sidecar body: canonical Phase 4bb-F format
`<json_sha256_hex>  <basename>\n` (two spaces between hash and
basename; one trailing newline; `sha256sum`-compatible).

Gitignore coverage (post-merge verified via `git check-ignore -v`):

```text
.gitignore:85:data/microstructure/	data/microstructure/successor-state/
.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json
.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json.sha256
```

Both files were never staged or committed; the merge introduces no
new tracked files under `data/microstructure/`. Filename was
derived via
`prometheus.research.microstructure.canonical_paths.derive_canonical_successor_state_path(...)`;
sidecar was written via `write_paired_sha256_sidecar(refuse_overwrite=True)`.

The previously recorded Phase 4bb-G raw successor-state JSON +
sidecar, Phase 4bg-B derived successor-state, Phase 4bi-D feature
successor-state, and Phase 4bj-G label successor-state remain at
their recorded gitignored paths and SHA256 digests, untouched and
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
- `git check-ignore -v data/microstructure/successor-state/`:
  `.gitignore:85:data/microstructure/	data/microstructure/successor-state/`.
- `git check-ignore -v` on the no-split determination JSON path:
  `.gitignore:85`.
- `git check-ignore -v` on the no-split determination sidecar path:
  `.gitignore:85`.
- SHA256 recomputation on every upstream artefact pre/post the
  merge: identical (see §9).
- SHA256 recomputation of the Phase 4bj-J no-split determination
  JSON: `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`
  (matches the value recorded in the sidecar).
- SHA256 recomputation of the Phase 4bj-J no-split determination
  sidecar: `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8`;
  sidecar parses correctly under the canonical Phase 4bb-F
  two-space format.
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-J modifies
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
| Phase 4bj-J no-split determination JSON (new local gitignored) | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` |
| Phase 4bj-J no-split determination sidecar (new local gitignored) | `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8` |

All twenty-one prior artefacts byte-for-byte unchanged across the
merge. The two new Phase 4bj-J artefacts remain at their recorded
SHAs and are gitignored / uncommitted. The Phase 4bb-D doubled-path
gate report remains valid at its recorded historical path; it was
not migrated, copied, renamed, deleted, or rewritten.

## 10. Manifest state preservation (if applicable)

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Governance labels |
| --- | --- | --- | --- | --- |
| Raw aggTrades (`microstructure_raw_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Derived normalized aggTrades (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Feature aggTrades (`microstructure_features_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Label aggTrades (`microstructure_labels_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | unchanged |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant **preserved (never invoked)** by Phase 4bj-J
or by the merge.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. Phase 4bj-J explicitly **does not** mutate
this field on the original manifest; the Option D no-split
determination is encoded ONLY in the new sibling JSON at the
path recorded in §7. Any future reader that wishes to interpret
the label family as no-split must read the sibling JSON, never
the label manifest, and never assume `chronological_split_policy`
should be flipped on the label manifest. Label-family no-split
status is a governance state, not an empirical claim about edge.

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
  sidecar created on the branch remain at their recorded local
  gitignored paths and SHAs; the merge does not rewrite, move,
  copy, rename, or modify either file.
- No label parquet read for computation, modification, or
  recomputation (only SHA256 verification).
- No train / validation / test split artefact created.
- No within-day descriptive segmentation artefact created.
- No additional successor-state artefact created beyond the single
  no-split determination JSON.
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
- No label statistics computed beyond the documentation-level
  references already recorded in Phase 4bj-B / 4bj-C / 4bj-D /
  4bj-E / 4bj-G / 4bj-H / 4bj-I.
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

The Phase 4bj-J merge does NOT, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels / features / OI /
  funding context / derivatives flow into trading signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- empirical label evaluation, label statistics computation,
  histogram / distribution / quantile / autocorrelation /
  cross-horizon-relationship analysis on the label parquet, or
  reading the label parquet for analysis (the merge only verifies
  the label parquet SHA256);
- split artefact creation (no train / validation / test partitions
  on disk; no within-day descriptive segmentation artefacts;
  recording a no-split determination as a sibling artefact is the
  only thing Phase 4bj-J does, and is encoded ONLY in the local
  gitignored JSON; no manifest mutation);
- mutating the label manifest's `chronological_split_policy` from
  `"not_yet_defined"` to any value;
- transitioning any manifest's `research_eligible` from `false` to
  `true`;
- transitioning any manifest's `eligibility_gate_status` from
  `pending` to `pass` or `fail`;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- Phase 4 canonical or Phase 5 authorisation;
- Phase 4bj-K (label diagnostic study plan), Phase 4bj-L (label
  diagnostic study execution), or any Phase 4bj-M / 4bj-N / 4bj-*
  successor in the labels arc;
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
- M0 amendment derived from Phase 4bj-J reasoning;
- broadening Phase 4bj-J no-split-determination language into
  binding cross-project governance beyond its docs + local-
  gitignored-output scope.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

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

Phase 4bj-J is now project-complete on `main` after this merge and
the merge-closeout commit. The microstructure aggTrades lineage
arc remains in its post-Phase-4bj-I state with respect to
artefacts: every dataset family (raw / derived / feature / label)
has a machine-readable sibling successor-state marker recorded as
a gitignored JSON artefact under
`data/microstructure/successor-state/`, every original manifest
remains byte-identical with `research_eligible: false` and
`eligibility_gate_status: "pending"`, and the label manifest's
`chronological_split_policy` remains `"not_yet_defined"`. Phase
4bj-J adds one more sibling artefact in the same canonical
namespace: a no-split determination JSON that records the Phase
4bj-I Option D decision for the locked single-day BTCUSDT
2025-01-15 label cell, along with a future-segmentation policy
reference (uniform 60s purge / embargo; neutral fixture
vocabulary; forbidden train / validation / test vocabulary). The
artefact is governance state, not empirical edge evidence. Labels
remain not signals. No successor phase is authorized. Per the
operator's instruction, the project remains paused; any future
phase requires a separately authorized prompt that satisfies the
Phase 4bk-A workflow standard, the Phase 4ak M0 twelve-clause
gate, and the Phase 4al refined no-rescue rule.

**Conditional next, NOT authorized:** Phase 4bj-K-equivalent
**Label Diagnostic Study Plan** (docs-only) is the cleanest
non-paused option. It would predeclare the set of allowed
descriptive label diagnostics, the per-horizon exclusion rules,
the leakage-check requirements, the output paths, the stop
conditions, the descriptive-only declaration, and the explicit
gating that any future Phase 4bj-L-equivalent (label diagnostic
study execution) would have to satisfy. Phase 4bj-K would
explicitly authorize none of: ML, strategy, signal construction,
backtests, acquisition, paper / shadow, live-readiness,
deployment, or exchange-write. Phase 4bj-K is **not** authorised
by this merge.
