# Phase 4aq Merge Closeout — V1-Arc Exit-Path Forensic Computation

## 1. Merge purpose

This document records the no-fast-forward merge of completed Phase
4aq (V1-Arc Exit-Path Forensic Computation) into `main`.

This is a docs-and-code research merge-closeout for the Phase 4aq
branch. It records the merge of the Phase 4aq standalone forensic
script, the Phase 4aq main memo, the Phase 4aq closeout, the
narrow `current-project-state.md` update, the Phase 4aq pre-merge
wording-correction commit, and this merge-closeout file.

This merge does not authorize any successor phase. It does not
authorize Phase 4ar, Phase 5, Phase 4 canonical, paper / shadow,
live-readiness, deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
credentials, or 5m / 1m / aggTrades / tick / mark-price 30m / 4h
data acquisition.

## 2. Merge summary

- Phase 4aq title: V1-Arc Exit-Path Forensic Computation.
- Merge branch: `phase-4aq/v1-arc-exit-path-forensic-computation`.
- Target branch: `main`.
- Main before merge: `4cad1f6444605f10366f86d448e77bfd401771db`
  (Phase 4ap merge on main).
- Phase 4aq main computation commit:
  `bfe9aafd5e87a4f008f5f4bfa7d1da7e26053360`.
- Phase 4aq closeout commit:
  `4dd5f6a36a1c76102d9d71a4c8849cc632381eba`.
- Phase 4aq correction commit:
  `b56ee090ce486f4efd6e3c3f812416bf32fc89b7`.
- Merge method: `--no-ff`.
- Initial merge commit SHA (pre-amend):
  `9f3620eb65d0cf320bb9b73f8ebf608e4e34bc11`.
- This merge-closeout has been amended exactly once after the
  initial merge commit to record this pre-amend SHA into the file.
  The post-amend live `main` SHA after the single self-reference
  amend pass is reported in the Phase 4aq final operator report.
  Infinite SHA self-reference chasing is not performed (see §
  "Self-reference handling note" below).

## 3. Files brought forward from Phase 4aq

This merge brings forward the following files from
`phase-4aq/v1-arc-exit-path-forensic-computation` into `main`:

- `scripts/phase4aq_v1_arc_exit_path_forensics.py` — standalone
  Phase 4aq forensic computation script. Reads existing local V1-arc
  trade-log artefacts only. No `prometheus.runtime/execution/persistence`
  imports; no exchange adapters; no `requests/httpx/aiohttp/websockets/urllib`;
  no `.env`; no credentials; no Binance API; no network I/O; no
  historical-script execution; no data acquisition; no data
  modification; no manifest modification; no existing-trade-log
  modification; ruff clean; py-compile clean.
- `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md`
  — Phase 4aq main memo (with two pre-merge wording corrections in
  §9.3 and §9.7 applied via the correction commit; see § 5).
- `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`
  — Phase 4aq closeout (with pre-merge correction note appended via
  the correction commit; see § 5).
- `docs/00-meta/current-project-state.md` — narrow update adding the
  Phase 4aq narrative paragraph and replacing the "Current phase:"
  block while preserving the prior Phase 4ap block as historical
  context.

This merge also creates:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_merge-closeout.md`
  — this merge-closeout file.

This merge does NOT bring forward the local Phase 4aq output bundle
under `data/research/phase4aq/`. Those local research outputs follow
the Phase 4ai / 4l / 4r / 4x convention of remaining gitignored,
not committed, and reproducible from the standalone script and
existing local V1-arc trade-log artefacts. They are not part of the
merged tree on `main`.

## 4. Phase 4aq computation status

`SUCCESSFUL_COMPUTATION`.

- Allowlisted V1-arc Phase-2 directories loaded: 23 directories ×
  2 symbols (BTCUSDT, ETHUSDT) = **46 (directory, symbol) artefact
  pairs**.
- Latest run subdirectory selected per directory.
- Canonical ledger per pair: Parquet preferred (Parquet selected in
  every loaded pair; JSON fallback not exercised).
- Total trades loaded: **973** (H0=154; R3=392; R1a=110;
  R1b-narrow=88; R2=229).
- Phase 4ap §11 required-field schema validation: **100% pass**.
- Phase 4ap §15 stop-trigger-domain inference: every loaded V1-arc
  historical artefact tagged `stop_trigger_domain =
  trade_price_backtest`; `mixed_or_unknown` was never assigned.
- Phase 4ap §13 timeframe rule preserved: 15m bar-extreme only;
  no 5m / 1m / aggTrades / tick / mark-price 30m / 4h / mark-price
  5m / mark-price 15m data was used or referenced.
- Phase 4ap §14 cost rule preserved: §11.6 = 8 bps slippage per
  side preserved verbatim; `cost_in_R / fee_in_R / funding_in_R`
  exact-from-fields; `estimated_slippage_in_R` descriptive only;
  the identity is not asserted.
- Phase 4ap §17 stop conditions: **SC-1 through SC-11 all PASS**.
- Phase 4ap §9 forbidden questions F1–F10: **zero performed**;
  recorded as `NOT_PERFORMED`.
- Local outputs: 11 artefacts under `data/research/phase4aq/`,
  generated locally and **not committed**.

## 5. Summary of the two pre-merge fixes

Two narrow report-wording corrections were applied to the Phase 4aq
main memo in correction commit
`b56ee090ce486f4efd6e3c3f812416bf32fc89b7`:

- **Q6 R3 ETH table row completed.** The Q6 threshold-touch table in
  §9.3 of the Phase 4aq main memo previously contained a placeholder
  `(see CSV)` for the R3 ETH row. The row was completed using the
  existing local Phase 4aq output CSV
  (`data/research/phase4aq/excursion_threshold_touch_rates.csv`),
  R-window default cost cell, default stop_domain_variant, default
  fill_variant, ETHUSDT, R3 (n=33; `frac_+1R = 0.424`,
  `frac_+2R = 0.182`, `frac_+3R = 0.030`). The values were read
  directly from the file; no new computation was performed.
- **Q10 favorable-before-stop wording corrected.** §9.7 of the
  Phase 4aq main memo previously implied the per-trade favorable-
  before-stop proxy values were available in "the per-trade dataset."
  The Phase 4aq output bundle does not include a separate named
  per-trade output file. The wording was corrected to state
  explicitly that population-level summaries are reported through
  the aggregate output artefacts and per-trade proxy values are
  computed internally by the Phase 4aq script but are not emitted
  as a separate named per-trade output file.

A short pre-merge correction note was appended to the Phase 4aq
closeout documenting both corrections.

These corrections are wording-only.

- **No computation result changed.**
- **No outputs were committed.**
- **No governance, verdict, lock, data, manifest, source, test, or
  strategy file changed.** No `.gitignore` change. No `src/prometheus/`
  change. No test change. No existing-script change. No data
  acquisition. No manifest creation or modification.

## 6. Implementation / governance review

This merge confirms:

- **New standalone script added on main:**
  `scripts/phase4aq_v1_arc_exit_path_forensics.py`.
- **New Phase 4aq memo and closeout brought forward on main:**
  `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md`
  and `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`.
- **Narrow `current-project-state.md` update brought forward** with
  Phase 4aq narrative paragraph and the new "Current phase:" block;
  prior Phase 4ap block preserved as historical context.
- **Merge-closeout file created** at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_merge-closeout.md`
  (this file).
- **No `src/prometheus/` modification.**
- **No test modification.**
- **No existing-script modification** (no historical Phase-2 / Phase-3
  / Phase-4i / Phase-4l / Phase-4r / Phase-4x script touched).
- **No data file modification** (no `data/raw/`, `data/normalized/`,
  `data/derived/` change).
- **No manifest modification** (no `data/manifests/` change; no
  `research_eligible` flag flipped; no v003 created).
- **No existing trade-log modification.**
- **No governance-document modification** beyond the narrow
  `current-project-state.md` update (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p /
  Phase 4q / Phase 4v / Phase 4w / Phase 4ak M0 governance change).
- **No retained verdict revised.**
- **No project lock changed.**
- **No strategy spec / threshold modified.**
- **No `.gitignore` modification.**
- **`data/research/phase4aq/` outputs remain local-only / gitignored
  / uncommitted**, reproducible from the standalone script and
  existing local V1-arc trade-log artefacts (matching Phase 4ai /
  4l / 4r / 4x precedent).

## 7. Research interpretation review

### What did Phase 4aq prove?

Phase 4aq produced a reproducible descriptive forensic snapshot of
V1-arc trade populations (H0, R3, R1a, R1b-narrow, R2) on existing
local 15m trade-price-backtest artefacts. The snapshot covers
MFE / MAE / net_R distributions, descriptive cost decomposition,
exit-reason breakdown, threshold-touch rates, and bar-resolution
ambiguity rates. The Phase 4ap V1-arc forensic plan was executed
exactly as predeclared, with all Phase 4ap §17 stop conditions
passing and zero Phase 4ap §9 forbidden question forms performed.

### What did Phase 4aq not prove?

Phase 4aq did not prove that any V1-arc population can be improved,
rescued, promoted, or hybridized. It did not prove that any V1-arc
verdict or project lock should change. It did not prove that
lower-timeframe data acquisition is necessary or justified. It did
not produce a new strategy candidate.

### Which original questions did it answer?

Phase 4ap descriptive Q1–Q14, within the limits of the existing 15m
schema. Q9 (`adverse_before_favorable_flag`) is recorded as
`NOT_AUDITABLE_FROM_EXISTING_FIELDS`. Q7 (favorable-before-stop) is
recorded as a labelled proxy.

### Which original questions remain open?

Phase 4ap forbidden questions F1–F10 are explicitly out of scope and
remain unaddressed. Any deeper sequencing question (true intrabar
event order, intra-15m-bar stop-vs-target sequencing, exact
mark-price trigger time) is unaddressed because it would require
lower-timeframe data not authorized by Phase 4aq.

### What does it mean for strategy research?

Phase 4aq provides descriptive context for understanding how V1-arc
trades unfolded relative to their MFE / MAE / cost / exit-reason
profile. It does not motivate strategy work. The cumulative
six-failure-mode rejection topology (R2 / F1 / D1-A / V2 / G1 / C1)
remains preserved, and Phase 4aq does not introduce any new
candidate.

### What does it mean for governance?

M0 admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase
4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption, and the Phase
4al / 4am / 4an / 4ao / 4ap chain are all preserved. Phase 4aq
does not amend any governance text. Phase 4aq is descriptive
research evidence only.

### What is the clean next step?

Operator review of the Phase 4aq descriptive results. No successor
phase is authorized. The clean next step is operator-driven only.
Acceptable separately-authorized future options include remain
paused, a narrower docs-only Phase 4aq interpretation memo, or a
future Phase 4ar-class consolidation memo. None of these is started
or authorized by this merge.

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

## 8. Retained verdict ledger

Preserved verbatim across this merge:

- **H0** remains FRAMEWORK ANCHOR.
- **R3** remains BASELINE-OF-RECORD.
- **R1a** remains RETAINED — NON-LEADING.
- **R1b-narrow** remains RETAINED — NON-LEADING.
- **R2** remains FAILED — §11.6.
- **F1** remains HARD REJECT.
- **D1-A** remains MECHANISM PASS / FRAMEWORK FAIL.
- **5m research thread** remains operationally CLOSED.
- **V2** remains HARD REJECT — terminal for V2 first-spec.
- **G1** remains HARD REJECT — terminal for G1 first-spec.
- **C1** remains HARD REJECT — terminal for C1 first-spec.

## 9. Preserved project locks

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- **§11.6** HIGH cost remains preserved. Any fee / slippage / funding
  decomposition reported by Phase 4aq is descriptive only and must
  not change the locked project-level cost reference or revise
  historical results.
- **§1.7.3** project-level locks remain:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- **Phase 3r §8** preserved.
- **Phase 3v §8** preserved.
- **Phase 3w §6 / §7 / §8** preserved.
- **Phase 4j §11** preserved.
- **Phase 4k** preserved.
- **Phase 4p** preserved.
- **Phase 4q** preserved.
- **Phase 4v** preserved.
- **Phase 4w** preserved.
- **Phase 4ak M0 governance** preserved (twelve-clause M0 gate +
  post-null cooldown + cooled-down families list + memo template).
- **Phase 4al / 4am findings** preserved.
- **Phase 4an inventory result** preserved.
- **Phase 4ao harmonization result** preserved.
- **Phase 4ap forensic plan** preserved.
- **Phase 4aq computation result** preserved as descriptive evidence
  only (no verdict / lock / governance implication; no successor
  authorization).

## 10. Boundary confirmations

This merge did NOT start or authorize:

- Phase 4ar;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- exit design;
- strategy design;
- parameter optimization;
- R3 optimization;
- R3-prime;
- R2-prime;
- R1a-prime;
- R1b-narrow-prime;
- H0-prime;
- strategy resurrection (V2-prime / V2-narrow / V2-relaxed / V2
  hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid /
  C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 /
  any cross-strategy hybrid);
- verdict revision;
- lock revision;
- M0 amendment;
- 5m research thread reopening;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h data acquisition;
- rerun of any historical strategy script;
- backtest;
- historical script execution;
- data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- production keys;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- WebSocket;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

## 11. Final recommendation

- **Recommended state remains paused.**
- **No successor phase is authorized by this merge.**
- The Phase 4aq descriptive results are now part of the project
  record on `main`. Operator may later separately authorize a
  narrower docs-only Phase 4aq interpretation memo, a future Phase
  4ar-class consolidation memo, or simply remain paused indefinitely.
- M0 mechanism-admissibility gate and post-null cooldown rule
  remain binding prospective governance for any future research
  lane.

## Self-reference handling note

A commit cannot contain its own SHA. This merge-closeout is committed
as part of the Phase 4aq merge into `main`. If a single self-reference
amend pass is used to record the merge SHA into this file after the
initial merge commit, the post-amend live `main` SHA is reported in
the final operator report, and infinite SHA self-reference chasing is
not performed. Otherwise the merge SHA is recorded in the final
operator report only.

## End of Phase 4aq merge-closeout
