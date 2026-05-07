# Phase 4ar Merge Closeout — V1-Arc Exit-Path Forensic Interpretation Memo

## 1. Merge purpose

This document records the no-fast-forward merge of completed Phase
4ar (V1-Arc Exit-Path Forensic Interpretation Memo) into `main`.

This is a **docs-only interpretation merge-closeout** for the Phase
4ar branch. It records the merge of the Phase 4ar interpretation
memo, the Phase 4ar closeout, the narrow `current-project-state.md`
update, and this merge-closeout file.

This merge does **not authorize Phase 4as or any successor phase**.
It does not authorize Phase 5, Phase 4 canonical, paper / shadow,
live-readiness, deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
credentials, or 5m / 1m / aggTrades / tick / mark-price 30m / 4h
data acquisition.

## 2. Merge summary

- **Phase 4ar title:** V1-Arc Exit-Path Forensic Interpretation Memo.
- **Merge branch:** `phase-4ar/v1-arc-exit-path-forensic-interpretation`.
- **Target branch:** `main`.
- **Main before merge:** `bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b`
  (Phase 4aq merge on main; verified equal to `origin/main` before
  the merge began).
- **Phase 4ar memo commit:**
  `d364981dddfb5d47359a42939d7ed91eb01d0f71`
  (`docs(phase-4ar): interpret v1-arc exit-path forensics`).
- **Phase 4ar closeout commit:**
  `ff7745f1c44b799943a900304a43084247e8e5d6`
  (`docs(phase-4ar): add closeout`).
- **Merge method:** `--no-ff` (no-fast-forward).
- **Initial merge commit SHA (pre-amend):**
  `ef52445e85baaea923a976c06a1321c32b9d56f3`.
- This merge-closeout has been amended exactly once after the
  initial merge commit to record this pre-amend SHA into the file.
  The post-amend live `main` SHA after the single self-reference
  amend pass is reported in the Phase 4ar final operator report.
  Infinite SHA self-reference chasing is not performed (see §
  "Self-reference handling note" below).

## 3. Files brought forward

This merge brings forward the following files from
`phase-4ar/v1-arc-exit-path-forensic-interpretation` into `main`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`
  — Phase 4ar main interpretation memo (19 sections covering
  executive summary, scope, repository verification, methodology,
  Phase 4aq evidence baseline, what Phase 4aq showed, what Phase
  4aq did NOT show, per-population interpretation, per-evidence-
  theme interpretation, exit-architecture interpretation boundary,
  lower-timeframe interpretation boundary, governance
  interpretation, forbidden interpretations, allowed
  interpretations, recommendation, implementation / governance
  review, plain-English research interpretation review, verdict
  and lock preservation, end-of-memo note).
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`
  — Phase 4ar closeout.
- `docs/00-meta/current-project-state.md` — narrow update adding
  the Phase 4ar narrative paragraph and replacing the "Current
  phase:" block with a Phase 4ar description while preserving the
  prior Phase 4aq block as historical context.

This merge also creates:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_merge-closeout.md`
  — this merge-closeout file.

This merge does NOT bring forward the local Phase 4aq output bundle
under `data/research/phase4aq/`. Those local research outputs follow
the Phase 4ai / 4l / 4r / 4x / 4aq convention of remaining
gitignored, not committed, and reproducible from the standalone
script and existing local V1-arc trade-log artefacts.

## 4. Phase 4ar interpretation status

- **Docs-only interpretation complete.**
- **No computation.**
- **No Phase 4aq script rerun.** `scripts/phase4aq_v1_arc_exit_path_forensics.py`
  was not re-executed by Phase 4ar.
- **No historical strategy script execution.** No Phase-2 / Phase-3
  / Phase-4i / Phase-4l / Phase-4r / Phase-4x script run.
- **No backtest.**
- **No data acquisition.** No 5m / 1m / aggTrades / tick / mark-
  price 30m / 4h / mark-price 5m / mark-price 15m data work.
- **No local `data/research/phase4aq/` output committed.** The local
  output bundle remains gitignored / not committed; reproducible
  from the committed standalone Phase 4aq script and existing
  local V1-arc trade-log artefacts.

## 5. Phase 4ar interpretation result

- **Phase 4aq is descriptive evidence only.** It documents how
  V1-arc trades unfolded under the locked Phase 4ap methodology on
  existing local 15m trade-price-backtest artefacts.
- **V1-arc trades had favorable excursion** (non-trivial MFE_R
  distributions: medians ~ 0.366R–1.036R across primary cells),
  **but favorable excursion did NOT, on average, translate into
  positive realized net_R** in the primary R-window default cell on
  either BTCUSDT or ETHUSDT. All five included populations (H0, R3,
  R1a, R1b-narrow, R2) showed negative `net_R_mean` (~ −0.114R to
  −0.443R) on the primary cell.
- **15m evidence is sufficient for descriptive V1-arc
  interpretation but not for true intrabar event-order certainty.**
  This is a structural limit of the existing trade-log schema, not
  an artefact of insufficient effort.
- **`adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`**
  for every loaded trade. Phase 4ap §12 / §13 explicitly forbid
  inferring sequence from final MFE / MAE alone or consulting
  lower-timeframe data in this phase.
- **`favorable_excursion_before_stop_proxy` is a labelled proxy
  only.** It is computed for STOP exits as `mfe_r > 0` but does
  not assert intrabar sequencing.
- **Threshold-touch rates are descriptive frequencies, not TP
  recommendations.** `frac_+1R` ranges ~ 0.18–0.57 and `frac_+3R`
  ranges ~ 0.00–0.08 across primary cells. Phase 4ap §9 F1 and F3
  explicitly forbid converting such frequencies into take-profit-
  multiple selections.
- **`estimated_slippage_in_R` is descriptive and estimated, not
  exact.** Derived from `slippage_bucket` mapped to per-side bps
  (LOW=1, MEDIUM=4, HIGH=8) with round-trip = 2 × per-side and
  notional from `notional_usdt` (or `abs(quantity) *
  entry_fill_price` fallback). The identity `cost_in_R == fee_in_R
  + estimated_slippage_in_R + funding_in_R` is **not asserted**.
  §11.6 = 8 bps slippage per side preserved verbatim.
- **Bar-resolution ambiguity is documented limitation only**, not
  authorization for lower-timeframe acquisition. BTCUSDT primary
  cells fall into the Phase 4al §14.C `2-10%` band; ETHUSDT primary
  cells fall into the `10-20%` band. Phase 4ar does NOT authorize
  5m / 1m / aggTrades / tick / mark-price acquisition. Phase 4ar
  does NOT reopen the 5m research thread (Phase 3t closure
  preserved).
- **No exit design, rescue, optimization, verdict revision, lock
  revision, or successor authorization follows from Phase 4ar.**
  The Phase 4aq evidence and Phase 4ar interpretation are
  descriptive research evidence only.

## 6. Per-population interpretation boundary

- **H0** remains FRAMEWORK ANCHOR. **No H0-prime** or framework-
  anchor revision. H0 forensic findings are baseline descriptive
  context only.
- **R3** remains BASELINE-OF-RECORD. **No R3 optimization**, **no
  R3-prime**, **no R3 rescue**, **no baseline-of-record revision**.
  R3 forensic findings are descriptive context for the V1-arc
  baseline-of-record only and cannot be converted into entry
  rules, exit rules, parameters, thresholds, take-profit
  multiples, trailing-stop policies, break-even rules, partial-
  exit policies, time-stop changes, or any new V1-arc strategy
  candidate.
- **R1a** remains RETAINED — NON-LEADING. **No R1a-prime** or
  promotion to leading status. The per-bar volatility-percentile
  filter is not "validated" by Phase 4aq descriptive evidence.
- **R1b-narrow** remains RETAINED — NON-LEADING. **No R1b-narrow-
  prime** or promotion. Small primary-cell sample size (n=10 BTC,
  n=12 ETH) requires extra caution; small-n results are not
  promoted.
- **R2** remains FAILED — §11.6. **No R2 rescue**, **no R2-prime**,
  **no §11.6 relaxation**. R2's cost-cell descriptive variation
  across LOW / default / HIGH (and the TRADE_PRICE stop-domain
  variant and limit-at-pullback fill variant) does not change the
  locked §11.6 cost reference.

## 7. Implementation / governance review

This merge confirms:

- **New Phase 4ar memo and closeout brought forward on main:**
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`
  and `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`.
- **Narrow `current-project-state.md` update brought forward** with
  the Phase 4ar narrative paragraph and the new "Current phase:"
  block; prior Phase 4aq block preserved as historical context.
- **Merge-closeout file created** at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_merge-closeout.md`
  (this file).
- **No `src/prometheus/` modification.**
- **No test modification.**
- **No script modification** (no Phase-2 / Phase-3 / Phase-4i /
  Phase-4l / Phase-4r / Phase-4x / Phase-4aq script touched; no
  new script added).
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
  / uncommitted**, reproducible from the committed standalone Phase
  4aq script and existing local V1-arc trade-log artefacts.

## 8. Research interpretation review (plain English)

### What did Phase 4ar prove?

Phase 4ar consolidated the Phase 4aq descriptive forensic evidence
into plain-English research and governance interpretation. It
recorded what the Phase 4aq evidence supports (descriptive V1-arc
trade-path observations under the locked methodology; structural-
limit observations about intrabar sequencing under the 15m schema;
descriptive cost decomposition) and what it does not support
(recoverable edge; exit redesign; parameter optimization; H0 / R3 /
R1a / R1b-narrow / R2 promotion or rescue; lower-timeframe
escalation; verdict / lock revision; M0 amendment; successor-phase
authorization).

### What did Phase 4ar not prove?

Phase 4ar did not prove that any V1-arc population can be improved,
rescued, promoted, or hybridized. It did not prove that any V1-arc
verdict or project lock should change. It did not prove that
lower-timeframe data acquisition is necessary or justified. It did
not produce a new strategy candidate. It performed no computation;
the interpretation rests entirely on the merged Phase 4aq evidence.

### Which original questions did it answer?

The Phase 4ar question — "What does the Phase 4aq V1-arc descriptive
forensic evidence mean, and what does it not mean, without turning
it into exit design, optimization, rescue, verdict revision, or
lock revision?" — is answered across §§6–14 of the Phase 4ar main
memo (what Phase 4aq showed; what Phase 4aq did NOT show; per-
population interpretation; per-evidence-theme interpretation; exit-
architecture boundary; lower-timeframe boundary; governance
boundary; forbidden interpretations; allowed interpretations).

### Which original questions remain open?

Phase 4ap forbidden questions F1–F10 remain explicitly out of scope
and unanswered. Any deeper sequencing question (true intrabar event
order, intra-15m-bar stop-vs-target sequencing, exact mark-price
trigger time) remains structurally unauditable from the existing
15m fields. The question of whether any future ex-ante hypothesis
could clear M0 admissibility and the post-null cooldown rule remains
operator-driven and is not advanced by Phase 4ar.

### What does it mean for strategy research?

Phase 4ar's interpretation supports the conclusion that the V1-arc
descriptive forensic snapshot is **complete, internally consistent,
and bounded by the locked methodology**, and that no aspect of it
authorizes V1-arc rescue, promotion, or successor-candidate
creation. The cumulative six-failure-mode rejection topology
(R2 / F1 / D1-A / V2 / G1 / C1) remains preserved. The Phase 4m
18-requirement validity gate, the Phase 4t 10-dimension scoring
matrix, the Phase 4ak twelve-clause M0 gate, the Phase 4ak post-
null cooldown rule, and the Phase 4al refined no-rescue rule remain
the binding admissibility framework for any future hypothesis.

### What does it mean for governance?

Phase 4ar reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8, Phase
3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption, Phase 4al refined
no-rescue rule + §13 boundary + §14 hierarchy, Phase 4am §11.A
audit findings, Phase 4an inventory, Phase 4ao harmonization, Phase
4ap forensic plan, and Phase 4aq computation result preserved as
descriptive evidence only. None is amended. Phase 4ar adds Phase
4ar interpretation result as descriptive interpretation only.

### What is the clean next step?

Operator review of the Phase 4ar interpretation. **No successor
phase is authorized.** The clean next step is operator-driven only.
Acceptable separately-authorized future options include remain
paused (recommended), a narrower docs-only archival synthesis memo,
or a future governance memo on a precise governance question. None
is started or authorized by this merge.

### What should we not do yet?

- No V1-arc successor candidates (R3-prime / R1a-prime /
  R1b-narrow-prime / R2-prime / H0-prime).
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

## 9. Retained verdict ledger

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

## 10. Preserved project locks

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- **§11.6** HIGH cost remains preserved. Any fee / slippage / funding
  decomposition reported by Phase 4aq remains descriptive only and
  must not change the locked project-level cost reference or revise
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
- **Phase 4ak** M0 governance preserved (twelve-clause M0 gate +
  post-null cooldown + cooled-down families list + memo template).
- **Phase 4al / 4am findings** preserved.
- **Phase 4an** inventory result preserved.
- **Phase 4ao** harmonization result preserved.
- **Phase 4ap** forensic plan preserved.
- **Phase 4aq** computation result preserved as descriptive
  evidence only.
- **Phase 4ar** interpretation result preserved as descriptive
  interpretation only.

## 11. Boundary confirmations

This merge did NOT start or authorize:

- Phase 4as;
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
- rerun of `scripts/phase4aq_v1_arc_exit_path_forensics.py`;
- rerun of any historical strategy script;
- backtest;
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

## 12. Final recommendation

- **Recommended state remains paused.**
- **No successor phase is authorized by this merge.**
- Operator may later separately authorize:
  - a narrower docs-only archival synthesis memo reorganising the
    combined Phase 4an / 4ao / 4ap / 4aq / 4ar narrative into a
    single archival-friendly summary;
  - a future governance memo on a precise governance question (for
    example, an explicit operator decision about whether to add
    `data/research/` to `.gitignore` formally, or an explicit
    operator decision about mark-price stop-domain forensic
    admissibility under Phase 3v §8 + Phase 3r §8);
  - or no further action.
  None is started or authorized here.
- M0 mechanism-admissibility gate and post-null cooldown rule remain
  binding prospective governance for any future research lane.

## Self-reference handling note

A commit cannot contain its own SHA. This merge-closeout is committed
as part of the Phase 4ar merge into `main`. If a single self-
reference amend pass is used to record the pre-amend merge SHA into
this file after the initial merge commit, the post-amend live `main`
SHA is reported in the final operator report, and infinite SHA
self-reference chasing is not performed. Otherwise the merge SHA is
recorded in the final operator report only.

## End of Phase 4ar merge-closeout
