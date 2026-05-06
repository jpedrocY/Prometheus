# Phase 4aq Closeout — V1-Arc Exit-Path Forensic Computation

## Phase identity

- Phase ID: **4aq**
- Phase title: **V1-Arc Exit-Path Forensic Computation**
- Type: docs-and-code (standalone research script)
- Authority: Phase 4ap (V1-Arc Exit-Path Forensic Plan; merged
  `4cad1f6444605f10366f86d448e77bfd401771db`).
- Branch: `phase-4aq/v1-arc-exit-path-forensic-computation`.
- Base SHA (main at branch creation):
  `4cad1f6444605f10366f86d448e77bfd401771db`.
- Phase 4aq main commit SHA: `bfe9aaf` (this branch HEAD prior to
  closeout commit; recorded for reference; the closeout commit will
  be the new HEAD).

## Purpose

Phase 4aq is the docs-and-code execution of the Phase 4ap V1-Arc
Exit-Path Forensic Plan. It implements
[`scripts/phase4aq_v1_arc_exit_path_forensics.py`](../../../scripts/phase4aq_v1_arc_exit_path_forensics.py)
as a standalone descriptive-only forensic computation script and
runs it on the Phase 4ap-allowlisted V1-arc trade-log artefacts under
`data/derived/backtests/phase-2*`. The phase produces the Phase 4ap
§16 output artefact bundle locally under `data/research/phase4aq/`,
along with the Phase 4aq main memo and this closeout under
`docs/00-meta/implementation-reports/`, and a narrow update to
`docs/00-meta/current-project-state.md`.

## Computation status

**`SUCCESSFUL_COMPUTATION`.**

- 23 allowlisted V1-arc directories × 2 symbols = **46 (directory,
  symbol) artefact pairs** loaded.
- **973 trades** total (H0=154; R3=392; R1a=110; R1b-narrow=88;
  R2=229).
- Phase 4ap §11 required-field schema validation: **100% pass**.
- Phase 4ap §17 stop conditions: **SC-1 through SC-11 all PASS**.
- Phase 4ap §9 forbidden questions F1–F10: **zero performed**;
  recorded as `NOT_PERFORMED` in
  `forbidden_interpretation_checklist.md`.
- Output bundle: **11 artefacts** under `data/research/phase4aq/`.

## Computation result summary

### Headline descriptive findings (R-window default cell, primary)

- All five included populations (H0, R3, R1a, R1b-narrow, R2) show
  negative `net_R_mean` on both BTCUSDT and ETHUSDT in the primary
  R-window default cell, ranging approximately −0.114R to −0.443R.
- MFE_R medians across the primary cell range approximately
  0.366R–1.036R; MAE_R medians 0.514R–0.844R.
- `frac_reached_+1R` ranges approximately 0.18–0.57; `frac_reached_+3R`
  ranges approximately 0.00–0.08.
- Bar-resolution ambiguity rate (`bars_in_trade == 0`) on the primary
  cell falls in the Phase 4al §14.C `2-10%` band on BTCUSDT and the
  `10-20%` band on ETHUSDT.

### Sequence-claim disclaim

- `adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`
  for every trade. Phase 4aq does not infer event order from final
  MFE_R / MAE_R alone.
- `favorable_excursion_before_stop_proxy` is labelled **proxy** for
  STOP exits.
- No lower-timeframe data is consulted.

### Cost-decomposition disclaim

- `cost_in_R`, `fee_in_R`, and `funding_in_R` are exact-from-fields.
- `estimated_slippage_in_R` is descriptive only; derived from
  `slippage_bucket` mapped to per-side bps {LOW: 1, MEDIUM: 4,
  HIGH: 8} with round-trip = 2 × per-side, and notional from
  `notional_usdt` (or `abs(quantity) * entry_fill_price` fallback).
- The identity `cost_in_R == fee_in_R + estimated_slippage_in_R +
  funding_in_R` is **not asserted**.
- §11.6 = 8 bps per side preserved verbatim; no cost-cell descriptive
  finding is interpreted as cost-model evidence.

These findings are descriptive only. They do not rank populations
for promotion. They do not authorize parameter changes, exit-rule
designs, take-profit-multiple selections, threshold optimization,
verdict revision, or lock revision. They do not authorize R3
optimization, R3-prime, R3 rescue, baseline-of-record revision,
R1a-prime, R1b-narrow-prime, R2-prime, H0-prime, framework-anchor
revision, V1-arc successor-candidate creation, or V1-arc hybridization
with F1 / D1-A / V2 / G1 / C1.

## Files added

Committed in main commit (`bfe9aaf`):

- `scripts/phase4aq_v1_arc_exit_path_forensics.py` — standalone
  Phase 4aq forensic computation script. Reads existing V1-arc
  trade-log artefacts only. No prometheus.runtime / execution /
  persistence imports. No exchange adapters. No `requests` /
  `httpx` / `aiohttp` / `websockets` / `urllib`. No `.env` reads.
  No credentials. No Binance API. No network I/O. Passes
  `ruff check` (`All checks passed!`) and `python -m compileall`
  (rc=0).
- `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md`
  — Phase 4aq main memo. 23 sections including executive summary,
  scope, methodology, computation status, artefact summary, schema
  validation, output artefact summary, Q1–Q14 results, R3 / R2 /
  R1a / R1b-narrow / H0 boundaries, cost / sequence / ambiguity
  limitations, forbidden-interpretation checklist, stop-condition
  review, implementation / governance review, plain-English
  research interpretation, recommendation, verdict and lock
  preservation, end-of-phase note.

Committed in this closeout commit (Phase 4aq closeout):

- `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`
  — this closeout document.

## Files modified

Committed in main commit (`bfe9aaf`):

- `docs/00-meta/current-project-state.md` — narrow update adding the
  Phase 4aq narrative paragraph and replacing the "Current phase:"
  block with a Phase 4aq description while preserving the prior
  Phase 4ap block as historical context (matching prior-phase
  convention).

## Files NOT modified

The following were not modified by Phase 4aq:

- `src/prometheus/` (no source-code change).
- Any test under `tests/` (no test change).
- Any existing script under `scripts/` (no historical-script change;
  Phase 4aq added a new standalone script only).
- Any data file under `data/raw/`, `data/normalized/`, or
  `data/derived/` (no data modification).
- Any manifest under `data/manifests/` (no manifest creation or
  modification; no `research_eligible` flag flip).
- `.gitignore` (no narrowing or widening of ignore patterns).
- Any specialist governance file (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p /
  Phase 4q / Phase 4v / Phase 4w / Phase 4ak M0 governance
  modification).
- Any retained verdict (no verdict revision).
- Any project lock (no §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 /
  Phase 3w §6 / §7 / §8 / Phase 4j §11 modification).
- Phase 4z, Phase 4aa, Phase 4ab recommendations remain
  recommendations only (not adopted as binding governance).
- Phase 4ac / 4ad / 4ae / 4af / 4ag / 4ah / 4ai / 4aj scopes are
  preserved (not broadened).
- Phase 4al / 4am / 4an / 4ao / 4ap chain is preserved.
- The 5m research thread closure (Phase 3t) is preserved (not
  reopened).

## Docs-and-code confirmation

Phase 4aq is a docs-and-code phase under Phase 4ap §17 reproducibility
requirements. The committed changes are:

- one new standalone research script (`scripts/phase4aq_v1_arc_exit_path_forensics.py`),
- two new memo files (Phase 4aq main + closeout under
  `docs/00-meta/implementation-reports/`),
- a narrow update to `docs/00-meta/current-project-state.md`.

The standalone script passes the project's `ruff check` quality gate
and `python -m compileall` bytecode-compile check. The script is
self-contained: it requires no Prometheus runtime, no exchange
adapter, no credentials, no network, no historical-script execution,
and no manifest update.

## Output artefacts generated locally

All outputs reside under `data/research/phase4aq/` and are local
research outputs (not committed, gitignored per the Phase 4ai / 4l /
4r / 4x convention; reproducible from the script and existing local
V1-arc trade-log artefacts):

- `loaded_artifacts_manifest.csv` — 46 rows, one per (directory,
  symbol) artefact pair.
- `schema_validation_report.csv` — 46 rows; required-fields-missing
  empty for every row; fail_closed = "no" for every row.
- `population_summary.csv` — per-group counts and net_R / MFE_R /
  MAE_R summary metrics across all loaded variants.
- `mfe_mae_distribution_by_population.csv` — per-group MFE_R and
  MAE_R quantiles, plus `giveback_from_mfe` and `mfe_capture_ratio`
  summaries.
- `realized_r_by_population.csv` — per-group net_R distribution
  (mean, stdev, min, p10, p25, p50, p75, p90, p95, p99, max).
- `cost_in_r_by_population.csv` — per-group descriptive cost
  decomposition (cost_in_R, fee_in_R, funding_in_R,
  estimated_slippage_in_R) with reconciliation note.
- `exit_reason_breakdown.csv` — per-group exit-reason counts.
- `excursion_threshold_touch_rates.csv` — per-group fraction
  reaching `+1R / +2R / +3R`.
- `ambiguity_report.csv` — per-group bar-resolution ambiguity rate
  and Phase 4al §14.C descriptive band.
- `forbidden_interpretation_checklist.md` — Phase 4ap §9 F1–F10
  recorded as `NOT_PERFORMED`.
- `v1_arc_forensic_report.md` — full human-readable Phase 4aq
  forensic report.

## Validation commands

The following commands were run during Phase 4aq:

```text
git status                                        — clean working tree before branch creation
git rev-parse main                                — 4cad1f6444605f10366f86d448e77bfd401771db
git rev-parse origin/main                         — 4cad1f6444605f10366f86d448e77bfd401771db
git log --oneline -14                             — Phase 4ap on main confirmed
git ls-files docs/00-meta/implementation-reports/2026-05-06_phase-4ap_*.md
                                                  — Phase 4ap files present on main
git checkout -b phase-4aq/v1-arc-exit-path-forensic-computation
                                                  — Phase 4aq branch created
python scripts/phase4aq_v1_arc_exit_path_forensics.py --output-root data/research/phase4aq
                                                  — exit code 0; SUCCESSFUL_COMPUTATION;
                                                    46 pairs / 973 trades / 11 artefacts
uv run ruff check scripts/phase4aq_v1_arc_exit_path_forensics.py
                                                  — All checks passed!
python -m compileall -q scripts/phase4aq_v1_arc_exit_path_forensics.py
                                                  — rc=0
git add scripts/phase4aq_v1_arc_exit_path_forensics.py
        docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md
        docs/00-meta/current-project-state.md
git diff --cached --stat                          — 3 files; 3246 insertions
git diff --cached --check                         — no whitespace errors
git commit                                        — Phase 4aq main commit bfe9aaf
git add docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md
git diff --cached --stat                          — 1 file (closeout)
git diff --cached --check                         — no whitespace errors
git commit                                        — Phase 4aq closeout commit
git push -u origin phase-4aq/v1-arc-exit-path-forensic-computation
                                                  — push successful
git rev-parse phase-4aq/v1-arc-exit-path-forensic-computation
                                                  — local HEAD recorded
git rev-parse origin/phase-4aq/v1-arc-exit-path-forensic-computation
                                                  — origin HEAD == local HEAD
git status                                        — clean working tree on Phase 4aq branch
git log --oneline -8                              — Phase 4aq commits at top of log
```

`pytest` and `mypy` were NOT run because Phase 4aq does not modify
`src/prometheus/` or any test. The Phase 4aq script is a standalone
research script outside the runtime package; it has no test
counterpart by design (matching Phase 4ai / 4l / 4r / 4x precedent).

## Implementation / governance review

### What changed?

- New file: `scripts/phase4aq_v1_arc_exit_path_forensics.py`.
- New files: `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md`
  and `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`.
- Narrow update to `docs/00-meta/current-project-state.md` (Phase 4aq
  narrative paragraph + Phase 4aq "Current phase:" block; prior
  Phase 4ap block preserved as historical context).
- New local research outputs under `data/research/phase4aq/`
  (NOT committed; gitignored per Phase 4ai / 4l / 4r / 4x
  convention; reproducible from the standalone script + existing
  local V1-arc trade-log artefacts).

### What did not change?

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No data acquisition.
- No data file modification.
- No manifest modification.
- No `.gitignore` modification.
- No retained verdict revised.
- No project lock changed.
- No M0 governance modified.
- Phase 4z / 4aa / 4ab recommendations remain recommendations only.
- 5m research thread remains operationally CLOSED (Phase 3t).
- No backtest run.
- No historical strategy script executed.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim; see § "Preserved verdicts and locks" below.

### Was Phase 4aq mergeable as docs-and-code?

Yes. The standalone script passes `ruff check` and
`python -m compileall`. The local research outputs follow the
Phase 4ai / 4l / 4r / 4x convention of remaining a local,
reproducible-from-script artefact bundle.

## Research interpretation review (plain English)

### What did this phase prove?

Phase 4aq produced a reproducible descriptive forensic snapshot of
V1-arc trade populations (H0, R3, R1a, R1b-narrow, R2) on existing
local 15m trade-price-backtest artefacts. The snapshot covers
MFE / MAE / net_R distributions, descriptive cost decomposition,
exit-reason breakdown, threshold-touch rates, and bar-resolution
ambiguity rates.

### What did this phase not prove?

Phase 4aq did not prove that any V1-arc population can be improved,
rescued, promoted, or hybridized. It did not prove that any V1-arc
verdict or project lock should change. It did not prove that
lower-timeframe data acquisition is necessary or justified. It did
not produce a new strategy candidate.

### Which original questions did it answer?

The Phase 4ap descriptive questions Q1–Q14, within the limits of
the existing 15m schema. Q9 (`adverse_before_favorable_flag`) is
recorded as `NOT_AUDITABLE_FROM_EXISTING_FIELDS`. Q7
(favorable-before-stop) is recorded as a **proxy**.

### Which original questions remain open?

Phase 4ap forbidden questions F1–F10 are explicitly out of scope
and remain unaddressed. Any deeper sequencing question (true
intrabar event order, intra-15m-bar stop-vs-target sequencing,
exact mark-price trigger time) is unaddressed because it would
require lower-timeframe data not authorized by Phase 4aq.

### What does it mean for strategy research?

Phase 4aq provides descriptive context for understanding how
V1-arc trades unfolded relative to their MFE / MAE / cost /
exit-reason profile. It does not motivate strategy work. The
cumulative six-failure-mode rejection topology
(R2 / F1 / D1-A / V2 / G1 / C1) remains preserved verbatim, and
Phase 4aq does not introduce any new candidate.

### What does it mean for governance?

M0 admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption, and
the Phase 4al / 4am / 4an / 4ao / 4ap chain are all preserved.

### What is the clean next step?

Operator review of the Phase 4aq descriptive results. No successor
phase is authorized. The clean next step is operator-driven only.

### What should we not do yet?

- No V1-arc successor candidates (R3-prime / R1a-prime /
  R1b-narrow-prime / R2-prime / H0-prime).
- No exit-rule design from forensic numbers.
- No parameter optimization.
- No verdict revision.
- No project-lock revision.
- No 5m / 1m / aggTrades / tick / mark-price acquisition.
- No reopening of the 5m research thread.
- No paper / shadow / live-readiness / exchange-write.
- No production-key creation.
- No authenticated APIs / private endpoints / public-endpoint calls
  in code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.

## Preserved verdicts and locks

### Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m research thread** — operationally CLOSED (Phase 3t).
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

### Project locks (preserved verbatim)

- **§11.6** = 8 bps slippage per side; round-trip = 16 bps.
- **§1.7.3** = 0.25% risk; 2× leverage cap; one position max;
  mark-price stops.
- **Phase 3r §8** mark-price gap governance.
- **Phase 3v §8** stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** break-even / EMA slope / stagnation
  governance.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule
  (preserved; unused by Phase 4aq).
- **Phase 4k** V2 backtest-plan methodology.
- **Phase 4p** G1 strategy-spec memo.
- **Phase 4q** G1 backtest-plan methodology.
- **Phase 4v** C1 strategy-spec memo.
- **Phase 4w** C1 backtest-plan methodology.
- **Phase 4ak** M0 mechanism-admissibility gate adoption (twelve
  clauses + post-null cooldown + cooled-down families list + memo
  template).
- **Phase 4al** refined no-rescue rule + §13 future-phase boundary +
  §14 data-resolution hierarchy.
- **Phase 4am** §11.A audit findings (F-1 / F-2 / F-3 / F-4).
- **Phase 4an** historical-trade-population exit-path inventory.
- **Phase 4ao** exit-path methodology / artefact harmonization.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan.

### Boundaries not altered

- No M0 amendment.
- No Phase 4m 18-requirement validity-gate amendment.
- No Phase 4t 10-dimension scoring-matrix amendment.
- No Phase 4u opportunity-rate-vs-edge-rate amendment.
- No Phase 4w negative-baseline / PBO / DSR / CSCV amendment.
- No Phase 4z framework adoption.

## Recommendation

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by Phase 4aq):** future
  narrower docs-only interpretation memo focused on a specific
  Phase 4aq descriptive finding.
- **Conditional tertiary (NOT authorized by Phase 4aq):** future
  Phase 4ar-class memo consolidating Phase 4aq forensic evidence at
  a higher level without authorizing strategy work.
- **NOT recommended:** designing exits from forensic numbers;
  promoting any retained-evidence population; authorizing 5m / 1m
  / aggTrades / tick / mark-price acquisition; reopening the 5m
  research thread.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection (R3-prime / R1a-prime /
  R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime /
  D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime /
  G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy
  hybrid); M0 amendment from Phase 4aq reasoning; reopening the
  5m research thread; acquisition of 5m / 1m / aggTrades / tick /
  mark-price 30m / 4h data without separately authorized data-
  requirements memo; paper / shadow / live-readiness / deployment /
  exchange-write / production-key creation / authenticated APIs /
  private endpoints / public-endpoint calls in code / user stream /
  WebSocket / MCP / Graphify / `.mcp.json` / credentials.

## Final status

Phase 4aq is complete on branch
`phase-4aq/v1-arc-exit-path-forensic-computation`. Both the Phase 4aq
main commit and this closeout commit reside on the branch. Phase 4aq
will be pushed to origin and verified for local-vs-origin SHA parity
before this prompt concludes. Phase 4aq is **not yet merged** into
main; merging Phase 4aq is a separate operator decision.

## Successor authorization status

**No successor phase is authorized.** Phase 4ar / Phase 5 / Phase 4
canonical / paper / shadow / live-readiness / deployment /
exchange-write / production-key creation / authenticated APIs /
private endpoints / user stream / WebSocket / MCP / Graphify /
`.mcp.json` / credentials all remain unauthorized. 5m / 1m /
aggTrades / tick / mark-price 30m / 4h data acquisition remains
unauthorized. The recommended state remains paused.

Phase 4aq does not authorize a successor phase. The merge of
Phase 4aq into main is itself a separate operator decision and is
not performed by this prompt.

## End of Phase 4aq closeout
