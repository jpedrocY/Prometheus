# Phase 4bm-A — Closeout

## Phase identity

- **Phase:** Phase 4bm-A — Multi-Day Normalization Design Memo
- **Type:** docs-only design memo
- **Tier:** Tier 1 (Full Phase) under
  `docs/00-meta/process/phase-risk-tiering-standard.md` (Phase 4bl-F)
- **Branch:**
  `phase-4bm-a/multi-day-normalization-design-memo`
- **Base commit (`main` / `origin/main` at branch creation):**
  `ac3475acd332978bfe0037a24e5004cec5e84efc` (Phase 4bl-F merge-closeout
  commit)
- **Predecessor project-complete phase:** Phase 4bl-F — Phase
  Risk-Tiering and Controlled Remediation Standard
- **Status:** branch-complete; not merged; not project-complete

## Summary

Phase 4bm-A authored the v002 multi-day analogue of the Phase 4bc
v001 single-day normalization design memo. It defines the future
normalized derived dataset family
`microstructure_normalized_aggtrades_v001` with `dataset_version=v002`
that any future operator-authorized Phase 4bm-B implementation phase
must produce from the Phase 4az / Phase 4bl-C v002 multi-day BTCUSDT
aggTrades raw archive.

Key design decisions recorded:

- Dataset identity reuses the existing v001 family name with a new
  `dataset_version=v002`, mirroring the raw family's naming pattern
  (`microstructure_raw_aggtrades_v001` carries both `dataset_version=v001`
  for the single-day Phase 4az dataset and `dataset_version=v002` for
  the 90-day Phase 4bl-C dataset).
- The 19-column `NORMALIZED_SCHEMA_V001` contract is preserved
  byte-for-byte from Phase 4bc / Phase 4bd. Schema version is
  unchanged at `v001`. No new columns. No removed columns. No
  reordering. No dtype changes. Decimal-as-string for `price` and
  `quantity` is preserved verbatim; float storage forbidden.
- Per-day parquet partition layout is preserved from Phase 4bd: one
  parquet per `(symbol, utc_date)` under
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`.
  Total expected output: 90 parquets, 90 paired `.sha256` sidecars in
  canonical Phase 4bb-F format, plus one multi-day index manifest.
- One multi-day index manifest at
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`
  aggregates all 90 per-day parquet files via a `per_file_inventory`
  field, mirroring the v002 raw manifest's shape. Per-day
  sub-manifests are not produced; the multi-day index manifest is
  the single source of truth for the v002 derived family.
- Lineage citations: every per-row constant column and every
  manifest-level lineage field cites the v002 raw manifest SHA, the
  Phase 4bl-D-R PASS gate report id and SHA, the Phase 4bl-E
  successor-state SHA, and per-row the source raw zip SHA for that
  date.
- Eligibility model: the Phase 4ba 5-stage ladder applies to the v002
  derived family in its own right, independently of the v001 derived
  family's existing Stage-3 admissibility. Stage-0 reachable only
  after a future Phase 4bm-B execution. Stage transitions remain
  sibling successor-state JSON artefacts, never in-place manifest
  mutations. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant must be preserved end-to-end by any future
  Phase 4bm-B.
- The forbidden columns list is preserved verbatim from Phase 4bc.
  The forbidden inputs list is preserved and explicitly extends to
  exclude all v001 raw artefacts as direct lineage references (the
  Phase 4az 2025-01-15 zip is included by virtue of being part of
  the v002 90-day archive, but its lineage is cited via the v002
  raw manifest, not via a v001 manifest reference).
- All sidecars produced by any future Phase 4bm-B must conform to
  the Phase 4bb-F canonical sidecar format
  (`<sha>  <basename>\n`; two spaces; trailing LF; no CRLF; no BOM).
  The Phase 4bl-F R-SIDECAR-CRLF rule is a **remediation rule** for
  pre-existing non-canonical sidecars; it does not apply to forward
  writes by Phase 4bm-B.
- A 65-criterion validation contract is predeclared for any future
  Phase 4bm-B execution: 10 source-artefact precondition checks, 21
  per-day normalization checks (Phase 4bc / 4bd 27-check suite
  applied across 90 dates with multi-day extensions), 8 aggregate /
  multi-day checks, 10 lineage / immutability checks, 12 governance
  / boundary checks, and 4 quality-gate checks.
- The future phase ladder is named: Phase 4bm-B (implementation),
  Phase 4bm-C (structural QA), Phase 4bm-D (derived-family
  eligibility-gate), Phase 4bm-E (research-eligibility decision),
  Phase 4bm-F (successor-state recording). Each requires separate
  authorization. **None is authorized by Phase 4bm-A.**

The memo invokes nine Phase 4bl-F reusable non-authorization blocks
verbatim (`N-ACQUISITION`, `N-ENDPOINT`, `N-CREDENTIALS`, `N-MANIFEST`,
`N-GATE-RERUN`, `N-SUCCESSOR-STATE`, `N-DERIVATION`,
`N-DIAGNOSTICS-ML-STRATEGY`, `N-PHASE-5`, `N-VERDICT-LOCK`).

The Phase 4bd through Phase 4bl-F history is preserved verbatim.
Every retained verdict and every project lock is preserved verbatim.
The Phase 4aw `flip_research_eligible(...)` always-raises invariant
is preserved (never invoked). The Phase 4bb-F canonical path policy
is preserved (Phase 4bm-A's design follows it verbatim for sidecar
format and path placement). No actual manifest was modified. No data
was acquired. No gate was rerun. No successor-state artefact was
created. No authorization of any successor phase was issued.

## Files added (2)

| File | Purpose |
| --- | --- |
| `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_multi-day-normalization-design-memo.md` | The 13-section Phase 4bm-A design memo. |
| `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_closeout.md` | This closeout. |

## Files modified narrowly (1)

| File | Nature of change |
| --- | --- |
| `docs/00-meta/current-project-state.md` | Narrow Phase 4bm-A paragraph addition; new "Current phase:" block; prior Phase 4bl-F "Current phase:" block preserved as historical context. |

## Files NOT modified

- `src/prometheus/` (unchanged)
- `tests/` (unchanged)
- `scripts/` (unchanged)
- `pyproject.toml` (unchanged)
- `README.md` (unchanged)
- `.gitignore` (unchanged)
- `.gitattributes` (unchanged)
- MCP files (unchanged)
- All `data/microstructure/` artefacts (unchanged; byte-identical
  pre/post; the v002 raw manifest, raw zips, raw zip sidecars,
  acquisition log, Phase 4bl-D-R PASS gate report, Phase 4bl-E
  successor-state, and every other prior artefact)
- All prior phase implementation reports and merge-closeouts
  (unchanged)
- `docs/00-meta/process/` standards (unchanged; Phase 4bm-A invokes
  the Phase 4bl-F nine reusable non-authorization blocks verbatim
  but does not amend the standard)

## Validation

- `git status` — clean except for the tracked Phase 4bm-A docs and
  the pre-existing untracked `.claude/scheduled_tasks.lock` and
  `data/research/` entries.
- `git diff --check` — clean.
- `ruff` / `mypy` / `pytest` — **not run** (no source / test /
  script / configuration file was modified). Per the
  operator-report standard, this closeout does not claim those gates
  were exercised.

## Boundary confirmations (all true)

- No `data/microstructure/` write outside the allowed surface
  (the allowed surface is empty for Phase 4bm-A).
- No actual manifest modification.
- No `research_eligible` flip on any actual manifest.
- No `eligibility_gate_status` transition on any actual manifest.
- No `chronological_split_policy` change on any actual manifest.
- No gate rerun.
- No new gate report.
- No new successor-state artefact.
- No data acquired, downloaded, or fetched.
- No Binance / public / private endpoint contacted.
- No WebSocket opened.
- No credential used.
- No `.env` read or created.
- No `.mcp.json` read or created.
- MCP and Graphify not enabled.
- No normalization, derivation, features, labels, diagnostics,
  ML, strategy, signals, or backtests produced.
- No PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output computed.
- No retained verdict revised.
- No project lock changed.
- No M0 governance amended.
- No prior phase result rewritten.
- No prior governance memo modified.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).
- Phase 4bb-F canonical path policy preserved.
- Phase 4bl-F R-SIDECAR-CRLF rule preserved (Phase 4bm-A does not
  invoke it; it is a remediation rule and does not apply to forward
  design memos).
- Phase 4bl-D raw multi-day eligibility gate (33 checks) preserved.
- Phase 4bl-E raw v002 successor-state preserved.
- Phase 4bd v001 normalized parquet, v001 derived manifest, and
  Phase 4bg-B v001 successor-state preserved.
- Phase 4bd through Phase 4bl-F history preserved verbatim.

## Retained verdict ledger preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow
RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT;
D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY
CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec;
G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT —
terminal for C1 first-spec.

## Preserved project locks

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% /
2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause
gate + post-null cooldown + cooled-down families list + memo
template; Phase 4al refined no-rescue rule + §13 boundary + §14
hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises
invariant; Phase 4bb-F canonical path policy; Phase 4bl-F tier
model + R-SIDECAR-CRLF rule + nine reusable non-authorization
blocks.

## Successor authorization

**No successor authorized.**

Phase 4bm-A does not authorize:

- Phase 4bm-A merge phase;
- Phase 4bm-B (Multi-Day Normalization Implementation);
- Phase 4bm-C (Multi-Day Normalized Dataset Structural QA Memo);
- Phase 4bm-D (Multi-Day Derived-Family Eligibility-Gate Design +
  Implementation + Execution);
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility
  Decision Memo);
- Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* / 4bq-* (multi-day diagnostics / split arcs);
- Phase 5;
- Phase 4 canonical;
- normalization execution;
- features;
- labels;
- diagnostics;
- ML;
- strategy;
- backtests;
- acquisition (additional aggTrades / 5m / 1m / tick / mark-price
  30m / 4h / order-book / spot / cross-venue / funding /
  open-interest);
- exchange-write;
- paper / shadow;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- live WebSocket implementation;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials;
- any change to retained verdicts or project locks;
- any modification of any prior phase result.

## Recommended state

**Remain paused.**

The operator has signalled an intent to pause for a broader project
discussion (complexity, phase usefulness, possible energy-market
sibling project) before any technical successor is authorized. Phase
4bm-A satisfies the Phase 4bl-F merge-closeout's recommended
"Conditional next, NOT authorized" by producing the design memo
analogue of Phase 4bc for the v002 raw family. The recommended state
after Phase 4bm-A is to remain paused and let the operator decide
whether to authorize Phase 4bm-B or pivot to a different lane.

## Lifecycle status

Phase 4bm-A is **branch-complete only** by this work. Per the
Phase 4bk-A workflow standard, Phase 4bm-A is **not project-complete**
until a separately authorized merge phase records its merge-closeout
on `main`.

## Conditional next, not authorized

- Future operator-authorized Phase 4bm-A merge phase that merges
  this branch into `main` and records a Phase 4bm-A merge-closeout
  per `merge-closeout-standard.md`. Tier 1.
- Followed by an operator-driven discussion about project complexity,
  phase usefulness, and possible energy-market sibling project.
- Followed conditionally by a separately authorized future
  **Phase 4bm-B — Multi-Day Normalization Implementation** that
  implements this design exactly. Tier 1.

None of the above is authorized by Phase 4bm-A.
