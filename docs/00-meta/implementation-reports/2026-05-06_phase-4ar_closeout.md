# Phase 4ar Closeout — V1-Arc Exit-Path Forensic Interpretation Memo

## Phase identity

- Phase ID: **4ar**
- Phase title: **V1-Arc Exit-Path Forensic Interpretation Memo**
- Type: docs-only interpretation memo
- Authority: Phase 4aq (V1-Arc Exit-Path Forensic Computation;
  merged on `main` at `bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b`).
- Branch: `phase-4ar/v1-arc-exit-path-forensic-interpretation`.
- Base SHA (main at branch creation):
  `bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b`.
- Phase 4ar memo commit SHA:
  `d364981dddfb5d47359a42939d7ed91eb01d0f71`.

## Purpose

Phase 4ar consolidates the already-merged Phase 4aq descriptive
forensic evidence into plain-English research and governance
interpretation. It performs no computation, runs no script, runs no
backtest, acquires no data, and modifies no code, tests, data,
manifests, governance docs, verdicts, locks, strategy specs,
thresholds, or `.gitignore`. It does not commit any
`data/research/phase4aq/` output. The phase produces the Phase 4ar
main interpretation memo, this closeout, and a narrow update to
`docs/00-meta/current-project-state.md`.

## Interpretation result

The Phase 4ar interpretation result is summarised as follows.

- **Phase 4aq is descriptive evidence only.** It documents how
  V1-arc trades unfolded under the locked Phase 4ap methodology on
  existing local 15m trade-price-backtest artefacts.
- **What Phase 4aq showed (in plain English):** all five included
  V1-arc populations (H0, R3, R1a, R1b-narrow, R2) had **negative
  mean net_R** in the primary R-window default cell on both
  BTCUSDT and ETHUSDT (~ −0.114R to −0.443R). Favorable excursion
  existed (MFE_R medians ~ 0.366R–1.036R) but did **not, on
  average, translate** into positive realized net_R. Threshold-
  touch rates exist as descriptive frequencies. Cost / fee /
  funding / estimated-slippage are descriptive context only with
  the identity not asserted; §11.6 preserved verbatim. Bar-
  resolution ambiguity is bounded but real at 15m (BTCUSDT cells
  in `2-10%` Phase 4al §14.C band; ETHUSDT cells in `10-20%`
  band). Existing fields cannot answer true event-order questions
  (`adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`;
  `favorable_excursion_before_stop_proxy` is a labelled proxy).
- **What Phase 4aq did NOT show:** no proof of recoverable edge;
  no proof that R3 can be improved; no proof that R2 was cost-only;
  no proof that R1a / R1b-narrow should be promoted; no proof that
  H0 should be revised; no proof that any exit rule, TP, SL,
  trailing stop, break-even rule, time stop, or partial-exit
  system should be adopted; no proof that 5m / 1m escalation is
  justified; no basis for verdict or lock revision.
- **Per-population interpretation:** H0 remains FRAMEWORK ANCHOR;
  R3 remains BASELINE-OF-RECORD (no R3 optimization / R3-prime /
  rescue / baseline revision); R1a / R1b-narrow remain RETAINED —
  NON-LEADING (no -prime / promotion); R2 remains FAILED — §11.6
  (no rescue / R2-prime / §11.6 relaxation).
- **Per-evidence-theme interpretation:** MFE / MAE distributions
  describe trade-path behaviour; threshold-touch rates are
  descriptive frequencies (not TP recommendations); giveback-from-
  MFE is descriptive (no clamping); favorable-before-stop is a
  labelled proxy; adverse-before-favorable is non-auditable;
  cost decomposition is descriptive only; bar-resolution
  ambiguity is documented limitation; R-window vs sensitivity / V-
  window separation is binding interpretation discipline.
- **Exit-architecture interpretation boundary:** Phase 4aq
  audited V1-arc exit architecture descriptively at 15m
  resolution but does NOT support exit design / TP-SL selection /
  optimal-winner-management inference / trailing-stop, break-
  even, partial-exit, or time-stop justification / rescue of
  failed entries.
- **Lower-timeframe interpretation boundary:** bar-resolution
  ambiguity bands are descriptive limitation only. Phase 4ar does
  NOT authorize 5m / 1m / aggTrades / tick / mark-price 30m / 4h
  / mark-price 5m / mark-price 15m data acquisition. Phase 4ar
  does NOT reopen the 5m research thread (Phase 3t closure
  preserved). Any future lower-timeframe measurement-layer
  discussion would require separate operator authorization and
  must satisfy Phase 4al §14 and Phase 4ao §13.3.
- **Governance interpretation:** Phase 4aq is descriptive
  evidence only. M0 admissibility, post-null cooldown, §11.6,
  §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase
  4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase
  4ak adoption, Phase 4al refined no-rescue + §13 / §14, Phase
  4am §11.A audit, Phase 4an inventory, Phase 4ao harmonization,
  Phase 4ap forensic plan, and Phase 4aq computation result —
  all preserved.

## Files added

Committed in memo commit (`d364981`):

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`
  — Phase 4ar main interpretation memo (19 sections).

Committed in this closeout commit:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`
  — this closeout.

## Files modified

Committed in memo commit (`d364981`):

- `docs/00-meta/current-project-state.md` — narrow update adding
  the Phase 4ar narrative paragraph and replacing the "Current
  phase:" block with a Phase 4ar description while preserving the
  prior Phase 4aq block as historical context (matching prior-phase
  convention).

## Files NOT modified

Phase 4ar did not modify any of the following:

- `src/prometheus/` (no source-code change).
- Any test under `tests/` (no test change).
- Any existing script under `scripts/` (no historical-script
  change; `scripts/phase4aq_v1_arc_exit_path_forensics.py` was
  not re-executed and not modified).
- Any data file under `data/raw/`, `data/normalized/`, or
  `data/derived/` (no data modification).
- Any manifest under `data/manifests/` (no manifest creation or
  modification; no `research_eligible` flag flip; no v003 created).
- `.gitignore` (no narrowing or widening of ignore patterns).
- Any specialist governance file (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p /
  Phase 4q / Phase 4v / Phase 4w / Phase 4ak / Phase 4al / 4am /
  4an / 4ao / 4ap / 4aq governance modification).
- Any retained verdict (no verdict revision).
- Any project lock (no §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8
  / Phase 3w §6 / §7 / §8 / Phase 4j §11 modification).
- Phase 4z, Phase 4aa, Phase 4ab recommendations remain
  recommendations only (not adopted as binding governance).
- Phase 4ac / 4ad / 4ae / 4af / 4ag / 4ah / 4ai / 4aj scopes are
  preserved (not broadened).
- Phase 4al / 4am / 4an / 4ao / 4ap / 4aq chain is preserved.
- The 5m research thread closure (Phase 3t) is preserved (not
  reopened).
- Local Phase 4aq output bundle under `data/research/phase4aq/`
  (not modified, not committed).

## Docs-only confirmation

Phase 4ar is a docs-only interpretation phase. The committed
changes are:

- one new memo (Phase 4ar main interpretation),
- one new closeout (this file),
- a narrow update to `docs/00-meta/current-project-state.md`.

No script was added or executed. No backtest was run. No data was
acquired. No code under `src/prometheus/` was modified. No test was
modified. No existing script was modified. No `.gitignore` change
was made. No `data/research/phase4aq/` output was committed.

## Validation commands

The following commands were run during Phase 4ar:

```text
git status                                 — clean working tree on main before branch creation
git rev-parse main                         — bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b
git rev-parse origin/main                  — bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b
git ls-files docs/00-meta/implementation-reports/2026-05-06_phase-4aq_*.md
                                           — Phase 4aq memo + closeout + merge-closeout present on main
git ls-files scripts/phase4aq_v1_arc_exit_path_forensics.py
                                           — Phase 4aq script present on main
git checkout -b phase-4ar/v1-arc-exit-path-forensic-interpretation
                                           — branch created from main
git diff --stat                            — 1 file (current-project-state.md) ahead of memo creation
git diff --check                           — no whitespace errors
git status --short                         — modified state file + new memo file (untracked) + transients
git add docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md
        docs/00-meta/current-project-state.md
git diff --cached --stat                   — 2 files; 1,332 insertions
git diff --cached --check                  — no whitespace errors
git commit                                 — Phase 4ar memo commit d364981
git add docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md
git diff --cached --stat                   — 1 file (closeout)
git diff --cached --check                  — no whitespace errors
git commit                                 — Phase 4ar closeout commit
git push -u origin phase-4ar/v1-arc-exit-path-forensic-interpretation
                                           — push successful
git rev-parse HEAD / branch / origin/branch
                                           — local HEAD == origin HEAD
git status                                 — clean working tree on Phase 4ar branch
git log --oneline -8                       — Phase 4ar commits at top
```

`ruff check`, `pytest`, and `mypy` were NOT run because Phase 4ar
is docs-only (no `src/prometheus/` modification, no test
modification, no script modification, no `scripts/` change of any
kind). This matches the docs-only convention used by Phase 4d, 4e,
4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o, 4p, 4q, 4s, 4t, 4u, 4v, 4w, 4y, 4z,
4aa, 4ab, 4ad, 4ag, 4ah, 4aj, 4ak, 4al, 4am (audit-only), 4an, 4ao,
and 4ap.

## Implementation / governance review

### What changed?

- New file: `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`.
- New file: this closeout at `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`.
- Narrow update to `docs/00-meta/current-project-state.md` (Phase
  4ar narrative paragraph + Phase 4ar "Current phase:" block; prior
  Phase 4aq block preserved as historical context).

### What did not change?

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No `data/research/phase4aq/` output committed.
- No data file / manifest / `research_eligible` flag / v003 change.
- No `.gitignore` modification.
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price acquisition.
- No reopening of the 5m research thread.
- No backtest run.
- No historical strategy script executed.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure is preserved.
The cost lock is preserved. The position / leverage / risk locks
are preserved. The stop-trigger-domain governance is preserved.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4ar is docs-only.

### Is the phase mergeable as docs-only?

Yes. Phase 4ar adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`.

## Research interpretation review (plain English)

### What did this phase prove?

Phase 4ar consolidated the Phase 4aq descriptive forensic evidence
into plain-English research and governance interpretation. It
recorded what the Phase 4aq evidence supports (descriptive V1-arc
trade-path observations, structural-limit observations about
intrabar sequencing under the 15m schema, descriptive cost
decomposition) and what it does not support (recoverable edge,
exit redesign, parameter optimization, R3 / R2 / R1a / R1b-narrow
/ H0 promotion or rescue, lower-timeframe escalation, verdict /
lock revision, M0 amendment, successor-phase authorization).

### What did this phase not prove?

Phase 4ar did not prove that any V1-arc population can be improved,
rescued, promoted, or hybridized. It did not prove that any V1-arc
verdict or project lock should change. It did not prove that
lower-timeframe data acquisition is necessary or justified. It did
not produce a new strategy candidate. It did not perform any
computation; the interpretation rests on the merged Phase 4aq
evidence.

### Which original questions did it answer?

The Phase 4ar question — "What does the Phase 4aq V1-arc descriptive
forensic evidence mean, and what does it not mean, without turning
it into exit design, optimization, rescue, verdict revision, or
lock revision?" — is answered across §6 (what Phase 4aq showed),
§7 (what Phase 4aq did NOT show), §8 (per-population
interpretation), §9 (per-evidence-theme interpretation), §10
(exit-architecture boundary), §11 (lower-timeframe boundary), §12
(governance boundary), §13 (forbidden interpretations), and §14
(allowed interpretations) of the Phase 4ar main memo.

### Which original questions remain open?

Phase 4ap forbidden questions F1–F10 remain explicitly out of scope
and unanswered. Any deeper sequencing question (true intrabar event
order, intra-15m-bar stop-vs-target sequencing, exact mark-price
trigger time) remains structurally unauditable from the existing
15m fields. The question of whether any future ex-ante hypothesis
could clear M0 admissibility and the post-null cooldown rule
remains operator-driven and is not advanced by Phase 4ar.

### What does it mean for strategy research?

Phase 4ar's interpretation supports the conclusion that the V1-arc
descriptive forensic snapshot is complete, internally consistent,
and bounded by the locked methodology, and that no aspect of it
authorizes V1-arc rescue, promotion, or successor-candidate
creation. The cumulative six-failure-mode rejection topology
(R2 / F1 / D1-A / V2 / G1 / C1) remains preserved. The Phase 4m
18-requirement validity gate, the Phase 4t 10-dimension scoring
matrix, the Phase 4ak twelve-clause M0 gate, the Phase 4ak
post-null cooldown rule, and the Phase 4al refined no-rescue rule
remain the binding admissibility framework for any future
hypothesis.

### What does it mean for governance?

Phase 4ar reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8, Phase
3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
Phase 4q, Phase 4v, Phase 4w, Phase 4ak, Phase 4al refined no-rescue
+ §13 / §14, Phase 4am §11.A audit findings, Phase 4an inventory,
Phase 4ao harmonization, Phase 4ap forensic plan, and Phase 4aq
computation result preserved as descriptive evidence only. None is
amended.

### What is the clean next step?

Operator review of the Phase 4ar interpretation. **No successor
phase is authorized.** The clean next step is operator-driven only.
Acceptable separately-authorized future options include remain
paused (recommended), a narrower docs-only archival synthesis memo,
or a future governance memo on a precise governance question. None
is started or authorized by Phase 4ar.

### What should we not do yet?

- No V1-arc successor candidates.
- No exit-rule design from forensic numbers.
- No parameter optimization.
- No verdict / lock revision.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price acquisition.
- No reopening of the 5m research thread.
- No paper / shadow / live-readiness / deployment / exchange-write
  / production-key creation.
- No authenticated APIs / private endpoints / public-endpoint calls
  in code / user stream / WebSocket / MCP / Graphify / `.mcp.json`
  / credentials.

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
  mark-price stops where applicable.
- **Phase 3r §8** mark-price gap governance.
- **Phase 3v §8** stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** break-even / EMA slope / stagnation
  governance.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule
  (preserved; unused by Phase 4ar).
- **Phase 4k** V2 backtest-plan methodology.
- **Phase 4p** G1 strategy-spec memo.
- **Phase 4q** G1 backtest-plan methodology.
- **Phase 4v** C1 strategy-spec memo.
- **Phase 4w** C1 backtest-plan methodology.
- **Phase 4ak** M0 mechanism-admissibility gate adoption (twelve
  clauses + post-null cooldown + cooled-down families list + memo
  template).
- **Phase 4al** refined no-rescue rule + §13 future-phase boundary
  + §14 data-resolution hierarchy.
- **Phase 4am** §11.A audit findings (F-1 / F-2 / F-3 / F-4).
- **Phase 4an** historical-trade-population exit-path inventory.
- **Phase 4ao** exit-path methodology / artefact harmonization.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** computation result preserved as descriptive
  evidence only.

### Boundaries not altered

- No M0 amendment.
- No Phase 4m 18-requirement validity-gate amendment.
- No Phase 4t 10-dimension scoring-matrix amendment.
- No Phase 4u opportunity-rate-vs-edge-rate amendment.
- No Phase 4w negative-baseline / PBO / DSR / CSCV amendment.
- No Phase 4z framework adoption.

## Recommendation

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by Phase 4ar):** narrower
  docs-only archival synthesis memo reorganising the combined
  Phase 4an / 4ao / 4ap / 4aq / 4ar narrative into a single
  archival-friendly summary.
- **Conditional tertiary (NOT authorized by Phase 4ar):** future
  separately authorized governance memo only if a precise
  governance question arises.
- **NOT recommended:** computation by default; 5m / 1m escalation
  by default; exit design; strategy work; verdict / lock revision;
  M0 amendment; reopening the 5m research thread.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection (R3-prime / R1a-prime /
  R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime /
  D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime
  / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy
  hybrid); M0 amendment from Phase 4ar reasoning; reopening the
  5m research thread; acquisition of 5m / 1m / aggTrades / tick /
  mark-price 30m / 4h data without separately authorized data-
  requirements memo; paper / shadow / live-readiness / deployment
  / exchange-write / production-key creation / authenticated APIs
  / private endpoints / public-endpoint calls in code / user
  stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials.

## Final status

Phase 4ar is complete on branch
`phase-4ar/v1-arc-exit-path-forensic-interpretation`. Both the
Phase 4ar memo commit and this closeout commit reside on the
branch. Phase 4ar will be pushed to origin and verified for local-
vs-origin SHA parity before this prompt concludes. Phase 4ar is
**not yet merged** into main; merging Phase 4ar is a separate
operator decision.

## Successor authorization status

**No successor phase is authorized.** Phase 4as / Phase 5 / Phase 4
canonical / paper / shadow / live-readiness / deployment /
exchange-write / production-key creation / authenticated APIs /
private endpoints / user stream / WebSocket / MCP / Graphify /
`.mcp.json` / credentials all remain unauthorized. 5m / 1m /
aggTrades / tick / mark-price 30m / 4h data acquisition remains
unauthorized. The recommended state remains paused.

Phase 4ar does not authorize a successor phase. The merge of
Phase 4ar into main is itself a separate operator decision and is
not performed by this prompt.

## End of Phase 4ar closeout
