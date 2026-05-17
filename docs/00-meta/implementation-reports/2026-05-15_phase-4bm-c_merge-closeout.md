# Phase 4bm-C Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-C — Multi-Day Normalized Structural QA Memo
- **Tier**: Tier 1 (analysis-and-docs)
- **Type**: descriptive structural QA, read-only on data
- **Branch merged**: `phase-4bm-c/multi-day-normalized-structural-qa-memo`
- **Base**: `main` at `1613cf19de874293a545866000f1788e64e83cb3` (Phase 4bm-B merge-closeout commit)
- **Predecessor**: Phase 4bm-B (Multi-Day Normalization Implementation, project-complete on `main`)

## §2 SHAs

- **Pre-merge `main` SHA**: `1613cf19de874293a545866000f1788e64e83cb3`
- **Pre-merge `origin/main` SHA**: `1613cf19de874293a545866000f1788e64e83cb3` (in sync)
- **Phase 4bm-C branch tip SHA**: `850f769` (`docs(phase-4bm-c): structural QA memo, closeout, current-project-state update`)
- **Merge commit SHA**: `1e22760dced013a1ca5dc8b6e0abc93e856f9b3a`
- **Merge commit message**: `docs(phase-4bm-c): merge multi-day normalized structural qa memo`
- **Post-merge `main` SHA**: to be filled at commit time of this merge-closeout file
- **Final `main` / `origin/main` SHA**: to be filled at commit time of this merge-closeout file

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-c/multi-day-normalized-structural-qa-memo -m "docs(phase-4bm-c): merge multi-day normalized structural qa memo"`
- **Strategy**: `ort` (git default; reported by git as "Merge made by the 'ort' strategy")
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used

## §4 Files Brought Forward

Three tracked files brought forward from the Phase 4bm-C branch into `main`:

1. `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_multi-day-normalized-structural-qa-memo.md` (NEW, 17-section structural QA memo)
2. `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_closeout.md` (NEW, 12-section closeout)
3. `docs/00-meta/current-project-state.md` (MODIFIED, +373 insertions, 0 deletions — Phase 4bm-C narrative paragraph + new "Current phase:" block; prior Phase 4bm-B "Current phase:" block preserved as historical context)

No source code, no tests, no scripts, no configuration, no `.gitignore`, no `.gitattributes`, no `pyproject.toml`, no `README.md`, no MCP files, no `data/microstructure/` artefacts, no prior phase reports modified.

## §5 Diff Summary

```text
docs/00-meta/current-project-state.md              | 373 +++++++++++++++
docs/00-meta/implementation-reports/
  2026-05-15_phase-4bm-c_closeout.md               | 140 ++++++
docs/00-meta/implementation-reports/
  2026-05-15_phase-4bm-c_multi-day-normalized-
  structural-qa-memo.md                            | 514 +++++++++++++++++++++
 3 files changed, 1027 insertions(+)
```

- 3 files changed
- 1,027 insertions
- 0 deletions
- All additive (no removals; no modifications outside `current-project-state.md`)
- `git diff --check` clean (no whitespace errors; no unresolved merge markers)

## §6 Result / Verdict

**STRUCTURAL_QA_PASS.** Phase 4bm-C is merged into `main` and recorded as project-complete via this merge-closeout.

The Phase 4bm-C verdict (descriptive only):

- **28 / 28** predeclared QA questions returned PASS
- **188 upstream immutability witnesses** byte-identical to recorded values
- **9,718,154 rows** row-level inspected on 5 sample dates (6.26% of total event count)
- Total event count = **155,153,449** (matches v002 manifest `total_event_count` exactly)
- Total parquet size = **1.40 GiB** (matches v002 manifest `total_size_bytes` exactly)
- The v002 derived family is structurally well-formed

The verdict is descriptive only. It does NOT transition the v002 manifest, does NOT flip `research_eligible`, does NOT transition `eligibility_gate_status`, and does NOT authorize any successor phase.

## §7 Local Gitignored Outputs (if any)

Phase 4bm-C produced no new local gitignored outputs. Phase 4bm-C was read-only against the existing local Phase 4bm-B v002 derived artefacts (90 Parquet files + 90 sidecars + 1 multi-day index manifest + 1 manifest sidecar) and the Phase 4bd v001 single-day parquet. All inspected local files preserved byte-identical to Phase 4bm-B recorded values.

The local v002 derived family at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` and the v002 index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (gitignored under `.gitignore:85`) remain present locally as Phase 4bm-B output; Phase 4bm-C did not write, mutate, or remove them.

## §8 Validation Results

### Merge preflight (pre-merge on Phase 4bm-C branch)

- `git status`: clean (only pre-existing untracked `.claude/scheduled_tasks.lock` and `data/research/`)
- `git diff --check`: clean (no whitespace errors; no merge markers)
- `git diff --stat main..phase-4bm-c/multi-day-normalized-structural-qa-memo`: 3 files / +1027 insertions / 0 deletions
- `git diff --name-status main..phase-4bm-c/multi-day-normalized-structural-qa-memo`: 1 M + 2 A (as expected)
- `git check-ignore -v data/microstructure/`: `.gitignore:85:data/microstructure/`
- `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/`: covered by `.gitignore:85`

### Optional spot-check (on local Phase 4bm-B v002 outputs)

- v002 derived multi-day index manifest SHA256 = `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (matches recorded value)
- v002 manifest paired `.sha256` sidecar SHA256 = `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` (matches recorded value)
- Sidecar body is canonical Phase 4bb-F format `<sha256_lowercase_hex>  <basename>\n` (two ASCII spaces; trailing LF); parses to the recomputed JSON SHA bit-for-bit

### Merge command output

- `Merge made by the 'ort' strategy.`
- 3 files changed, 1027 insertions(+)
- Conflicts: none
- Merge commit SHA: `1e22760dced013a1ca5dc8b6e0abc93e856f9b3a`

### Post-merge verification

- `git rev-parse HEAD`: `1e22760dced013a1ca5dc8b6e0abc93e856f9b3a`
- `git log --oneline -5 --decorate`: HEAD on `main` advances to the merge commit; predecessor commits visible (`850f769` branch tip; `1613cf1` prior `origin/main`; `57a2219` and `83d4e2b` Phase 4bm-B history)

### Whole-repo gates

Whole-repo `ruff` / `mypy` / `pytest` were NOT rerun by Phase 4bm-C (no source / test / script / configuration file was modified by either Phase 4bm-C or this merge). The latest authoritative whole-repo validation remains the Phase 4bm-B merge baseline:

- `ruff check .` PASS
- `mypy` strict PASS
- `pytest tests/research/microstructure/` 1156 passed + 1 skipped (the 1 skip is a labelled `pytest.skip` placeholder in `test_label_gate_report.py`)
- No new test regressions

## §9 Upstream Immutability Evidence

Phase 4bm-C inspected and confirmed **188 upstream immutability witnesses** byte-identical to recorded values. This merge introduces no new mutations; the immutability evidence carries forward unchanged:

- **4 governance witnesses**:
  - v002 raw manifest: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  - v002 acquisition log: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
  - Phase 4bl-D-R gate report: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`
  - Phase 4bl-E successor-state: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`
- **4 governance sidecars** (all paired `.sha256` files), all canonical Phase 4bb-F format, all matching recomputed SHAs
- **90 v002 raw zips** (each verified byte-identical to recorded Phase 4bl-C values and to per-row `source_file_sha256` lineage column inside the derived parquets)
- **90 v002 raw zip sidecars** (all canonical Phase 4bb-F format; all matching)
- **1 Phase 4bd v001 single-day parquet** at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` byte-identical to recorded SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` (Phase 4bm-A path-layout clarification holds; v002 family directory `microstructure_normalized_aggtrades_v001__v002/` cleanly coexists with v001 family directory `microstructure_normalized_aggtrades_v001/` with no collision at the 2025-01-15 date)

In addition, all 90 derived Parquet files and 90 derived sidecars produced by Phase 4bm-B were verified by Phase 4bm-C: every per-file recomputed SHA256 matches the v002 manifest's `per_file_inventory[*].file_sha256` entry; every paired `.sha256` sidecar matches; every sidecar is 103 bytes in canonical Phase 4bb-F format.

The Phase 4bd v001 derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` is untouched.

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bm-B output. Not modified by Phase 4bm-C. Not modified by this merge.
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bl-C. Not modified by Phase 4bm-C. Not modified by this merge.
- **Phase 4bd v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged from Phase 4bd. Not modified by Phase 4bm-C. Not modified by this merge.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. Phase 4bm-C never invoked it. The merge does not invoke it. The v002 multi-day index manifest is a sibling shape that does NOT use the single-file `MicrostructureManifest` data class; no path exists in this phase to flip any flag on any manifest.

## §11 Boundary Confirmations

All boundary confirmations preserved end-to-end by Phase 4bm-C and by this merge:

- No `data/microstructure/` write of any kind (Phase 4bm-C is read-only on data; merge brings forward only tracked docs)
- No actual manifest modification of any family (raw v001, raw v002, derived v001, derived v002 all byte-identical)
- No normalization run; no gate run; no successor-state recording; no diagnostic run
- No `research_eligible` flip on any manifest
- No `eligibility_gate_status` transition on any actual manifest
- No `chronological_split_policy` change on any actual manifest
- No data acquired; no Binance / public / private endpoint contacted; no WebSocket opened; no credential used; no `.env` read or created; no `.mcp.json` read or created; MCP and Graphify not enabled
- No features, labels, signals, ML, strategy, or backtest output computed
- No PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output computed
- No retained verdict revised
- No project lock changed
- No M0 governance amended; no post-null cooldown rule amended; no cooled-down families list amended; no memo template amended
- No Phase 4al refined no-rescue rule / §13 boundary / §14 hierarchy amended
- No Phase 4aw `flip_research_eligible(...)` always-raises invariant amended
- No Phase 4bb-F canonical path policy amended
- No Phase 4bl-F four-tier risk model / nine reusable non-authorization blocks / R-SIDECAR-CRLF standing rule amended
- No Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 amended
- No gate weakened
- No prior phase result rewritten
- No commit under `data/microstructure/`

## §12 Retained Verdict Ledger

All retained verdicts preserved verbatim:

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a / R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread OPERATIONALLY CLOSED per Phase 3t
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec

## §13 Preserved Project Locks

All project locks preserved verbatim:

- §11.6 = 8 bps per side
- Round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked)
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — forward writes use canonical LF natively)
- Phase 4am .. Phase 4bm-B results — all preserved verbatim

## §14 No-Rescue Constraints

Phase 4bm-C records a descriptive structural QA verdict on the v002 derived family produced by Phase 4bm-B. The verdict is descriptive only. It does NOT:

- revise or weaken any retained verdict (R2 / F1 / D1-A / V2 / G1 / C1 first-specs remain terminally rejected as recorded; H0 framework anchor, R3 baseline-of-record, and R1a / R1b-narrow retained-non-leading status all preserved)
- license rescue of any failed family, any rejected first-spec, any cooled-down lane, or the 5m research thread (which remains OPERATIONALLY CLOSED per Phase 3t)
- license parameter tuning, threshold optimization, classifier relaxation, regime-gate widening, stop-distance amendment, target-model amendment, time-stop amendment, or any post-hoc redesign of any historical or retained-evidence candidate
- license cross-strategy hybrids (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination)
- license -prime, -narrow, -extension, or -hybrid variants of any historical candidate
- license §11.6 cost-realism relaxation, §1.7.3 risk / leverage / one-position / mark-price stop amendment, or any other lock loosening
- license M0 amendment, post-null cooldown weakening, cooled-down families list shortening, or memo template alteration
- license use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs
- license use of 5m Q1–Q7 diagnostic outputs as rule-input candidates
- license any future ML training, model design, feature ranking, meta-labeling, strategy implementation, signal computation, backtest implementation, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated API access, private endpoint access, public-endpoint code calls, user-stream implementation, live WebSocket implementation, MCP enablement, Graphify enablement, or `.mcp.json` / credential creation

The v002 derived family being structurally well-formed at 28 / 28 QA PASS is necessary but not sufficient evidence for any of the above; sufficient evidence requires separately authorized subsequent phases under the established phase ladder (Phase 4bm-D → Phase 4bm-E → Phase 4bm-F → later research / feasibility / strategy / backtest phases under M0 admissibility and Phase 4al §14 hierarchy).

## §15 Successor Authorization

**No successor is authorized by this merge-closeout.**

This merge-closeout records that Phase 4bm-C is project-complete on `main`. It does NOT authorize:

- Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate
- Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision
- Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor
- Phase 5 / Phase 4 canonical
- Paper / shadow / live-readiness / deployment / exchange-write
- Production-key creation / authenticated APIs / private endpoints
- User-stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credential work
- Any additional acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- Any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual manifest

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-C is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The v002 derived family has descriptive structural QA confirmation (28 / 28 PASS) but no successor is authorized. The operator's broader pause decision pending project discussion (complexity assessment, phase usefulness review, possible energy-market sibling project) continues to apply.

**Conditional next, NOT authorized:**

- Future operator-authorized **Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate** (Tier 1 docs-and-code; the natural next step in the v002 lifecycle ladder by precedent of Phase 4bf for the Phase 4bd v001 derived family). Phase 4bm-D would translate the Phase 4bf 55-check derived-family eligibility-gate methodology into a v002-multi-day analogue and emit one gate report under `data/microstructure/gate-reports/normalized/` per the Phase 4bb-F canonical path policy. Phase 4bm-D is NOT authorized by this merge-closeout.

After any Phase 4bm-D merge, the recommended state would remain **remain paused** pending operator decision on the further conditional Phase 4bm-E (research-eligibility decision) and Phase 4bm-F (successor-state recording) ladder steps. None of those is authorized by this merge-closeout.

— end of Phase 4bm-C merge-closeout —
