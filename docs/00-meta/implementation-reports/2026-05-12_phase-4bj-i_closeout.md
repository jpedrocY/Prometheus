# Phase 4bj-I Closeout

## §1. Phase identity

- **Phase name:** Phase 4bj-I — Chronological Split Policy Design Memo.
- **Phase type:** docs-only design / governance memo.
- **Branch:** `phase-4bj-i/chronological-split-policy-design-memo`.
- **Base SHA:** `main` at `49d60b6e362294541b4f45f49c6e0b389b70b5b9` (Phase 4bj-H SHA-chain-fixup commit on top of the Phase 4bj-H merge-closeout anchor `65e9094a46eb6423ac6132ea394a62a7e860c55d`).
- **Project-completeness:** branch-complete only. Not project-complete until a separately authorized merge phase records the merge-closeout on `main`.

## §2. Status

- Phase 4bj-I is a docs-only design memo. It records the chronological split policy for the locked label-family cell `microstructure_labels_aggtrades_v001` / BTCUSDT / 2025-01-15.
- **Primary recommendation: Option D — declare the single-day cell insufficient for formal train / validation / test, and remain unsplit until multi-day data exists.**
- No data, manifest, parquet, sidecar, gate report, split artefact, or successor-state artefact was created, moved, copied, renamed, deleted, or modified.
- No `data/microstructure/` artefact was committed.
- The label manifest, label parquet, Phase 4bj-E gate report, Phase 4bj-G successor-state JSON, raw / derived / feature manifests, and all associated sidecars remain byte-identical and unmodified.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- The label manifest's `chronological_split_policy` remains `"not_yet_defined"`. No split-policy mutation was performed on the original manifest.

## §3. Local artefacts produced

**None.**

Phase 4bj-I produced no local gitignored artefact. The phase is strictly docs-only. No split artefact was created; the recorded recommendation is to defer split-artefact creation to a future separately authorized Phase 4bj-J-equivalent (or, alternatively, to record a no-split determination artefact under the same Phase 4bj-J-equivalent pattern).

## §4. Files added / modified (tracked)

- **Added:** `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-i_chronological-split-policy-design-memo.md` (the 18-section Phase 4bj-I design memo).
- **Added:** `docs/00-meta/implementation-reports/2026-05-12_phase-4bj-i_closeout.md` (this file).
- **Narrow modification:** `docs/00-meta/current-project-state.md` — new Phase 4bj-I narrative paragraph + new "Current phase:" Phase 4bj-I block; prior Phase 4bj-H "Current phase:" block preserved as historical context.

## §5. Files untouched

- All source modules under `src/prometheus/` (no edits).
- All tests under `tests/` (no edits).
- All scripts under `scripts/` (no edits).
- `.gitignore`, `pyproject.toml`, `README.md`, MCP files.
- All prior governance memos under `docs/00-meta/`, `docs/12-roadmap/`, `docs/03-strategy-research/`, `docs/05-backtesting-validation/`, `docs/06-execution-exchange/`, `docs/07-risk/`, `docs/08-architecture/`, `docs/09-operations/`, `docs/10-security/`, `docs/11-interface/`, and any other docs subtree (no edits) beyond the narrow `current-project-state.md` paragraph addition and "Current phase:" block update.
- All `data/microstructure/` artefacts (raw zip, raw manifest, raw zip sidecar, acquisition log, Phase 4bb-D gate report + sidecar, derived parquet + manifest + sidecar, normalized parquet + manifest + sidecar, feature parquet + manifest + sidecar, label parquet + manifest + sidecar, Phase 4bf / 4bi-B / 4bj-E gate reports + sidecars, Phase 4bg-B / 4bi-D / 4bj-G / 4bb-G successor-state artefacts + sidecars) — **all byte-for-byte unchanged**.

## §6. Validation

- `git status --short`: clean (only always-untracked scheduler lock and gitignored `data/research/`); no `data/microstructure/` artefact staged or modified.
- `git diff --check`: clean.
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bj-I modifies no source code, no tests, no scripts, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the Phase 4bb-F-implementation merge: `ruff check .` PASS, `mypy strict 120 source files` PASS, `pytest tests/research/microstructure/` 915 passed + 1 pre-existing labelled skip, whole-repo pytest 1698 passed + 1 skipped + 2 pre-existing simulation `KeyError: 'trade_count'` failures (unchanged from prior phases; not introduced by this phase).

## §7. Upstream artefact SHA preservation

No upstream artefact was read for computation, modification, or recomputation by Phase 4bj-I. All `data/microstructure/` artefacts are byte-identical pre/post and their SHA256s remain those recorded by the predecessor phases:

- raw manifest `a371edd4…`
- raw zip `f560c2e5…`
- raw zip sidecar `b80c2768…`
- acquisition log `f88b28b4…`
- Phase 4bb-D gate report `96f09159…`
- Phase 4bb-D gate report sidecar `93e68eb6…`
- Phase 4bb-G raw successor-state `ab6a82e7…`
- normalized parquet `2b3d6978…`
- original derived manifest `f6f0d947…`
- Phase 4bf derived gate report `dd4e0c1c…`
- Phase 4bg-B derived successor-state `8bcc7d01…`
- feature parquet `618d9b86…`
- feature manifest `624e8c5e…`
- Phase 4bi-B feature gate report `aa5d29c2…`
- Phase 4bi-D feature successor-state `8176aa3f…`
- label parquet `ef50038a…`
- label manifest `181a799c…`
- Phase 4bj-E label gate report `b0b5405b…`
- Phase 4bj-G label successor-state `ce7d3917…`

`mtime_ns` also unchanged for every artefact above.

## §8. Boundary confirmations

Phase 4bj-I did **NOT**:

- create any split artefact or no-split determination artefact;
- compute label statistics, descriptive distributions, or any other empirical label evaluation;
- read or process the label parquet beyond documentation-level reference to values already recorded in prior repo docs;
- create train / validation / test splits or other partitions;
- create new manifests, gate reports, or successor-state artefacts;
- rerun any gate (raw, derived, feature, or label);
- run kernels, normalizers, or any processing script;
- modify any manifest, parquet, sidecar, or raw zip;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any actual manifest (it remains `"not_yet_defined"` on the label manifest, by design);
- train ML, design ML architecture, rank features, or create meta-labeling;
- create a strategy, compute signals, run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- acquire data of any kind (order-book, mark-price, spot, cross-venue, funding, open-interest, additional aggTrades);
- call public, authenticated, or private Binance endpoints;
- open WebSockets or user streams;
- create or read credentials, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- modify project locks or revise retained verdicts;
- amend Phase 4ak M0 governance;
- merge into `main`;
- authorize Phase 4bj-J, Phase 4bj-K, Phase 4bj-L, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or any successor phase.

## §9. Retained verdict ledger preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.

## §10. Preserved project locks

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical path policy.

## §11. Successor authorization

**None.** No successor phase is authorized by Phase 4bj-I.

The following candidate successors are explicitly **NOT authorized**:

- Phase 4bj-J (or any equivalent Split Artefact Implementation / Recording or No-Split Determination Recording);
- Phase 4bj-K (or any equivalent Label Diagnostic Study Plan);
- Phase 4bj-L (or any equivalent Label Diagnostic Study Execution);
- any future ML feasibility memo;
- any future baseline ML diagnostic;
- any future failure-interpretation / fallback-selection memo;
- any future strategy hypothesis memo under M0;
- any future strategy spec memo;
- any future backtest plan memo;
- any future backtest execution phase;
- Phase 5;
- Phase 4 canonical;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue / funding / open-interest data acquisition;
- ML implementation, ML training, model selection, feature ranking, meta-labeling;
- strategy implementation, signal computation, backtest implementation;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production keys;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials.

## §12. Recommended state

**Remain paused.**

Phase 4bj-I is branch-complete only. Per the Phase 4bk-A workflow standard it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main`.

If the operator wishes to advance the label arc later, the cleanest non-paused option is a future docs + local-gitignored-output Phase 4bj-J-equivalent that records the Phase 4bj-I-recommended **no-split determination** as a sibling artefact under `data/microstructure/splits/` (preserving the label manifest byte-identically), or — if multi-day data is acquired separately first — a future split-artefact recording phase under the §5.3 / §6 / §7 / §9 rules of the Phase 4bj-I memo. That option is **not authorized by Phase 4bj-I**; it requires a separate operator authorization prompt that satisfies the Phase 4bk-A workflow standard, the Phase 4ak M0 twelve-clause gate, and the Phase 4al refined no-rescue rule.
