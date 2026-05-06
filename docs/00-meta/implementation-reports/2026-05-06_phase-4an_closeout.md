# Phase 4an Closeout — Historical Trade-Population Exit-Path Inventory Memo

## 1. Phase Identity

- Name: Phase 4an — Historical Trade-Population Exit-Path Inventory Memo.
- Type: docs-only inventory / closeout.
- Date: 2026-05-06.
- Phase memo: `docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`.

## 2. Branch

- Phase branch: `phase-4an/historical-trade-population-exit-path-inventory`.
- Forked from: clean main at `dfaa26a4e7f9a21957e0e465c7bb7de2e508a784`.

## 3. Base SHA

- Pre-Phase-4an main / origin/main: `dfaa26a4e7f9a21957e0e465c7bb7de2e508a784`
  (the Phase 4am merge-closeout merge commit).

## 4. Phase Commit SHA

- Phase 4an memo commit: `241d6a71bec61457a8b876572989d7550a9f1423`
  ("docs(phase-4an): inventory historical exit-path artefacts").
- Phase 4an closeout commit: recorded in §10 below after this file is
  staged and committed.

## 5. Purpose

This document is the Phase 4an closeout file. Its purpose is to:

- close out Phase 4an on the phase branch before the no-fast-forward merge
  to main;
- record the inventory result in summary form for repository-level
  governance review;
- preserve the retained verdict ledger and every project lock verbatim;
- confirm that Phase 4an did not modify source, tests, scripts, data,
  manifests, strategy specs, governance docs, retained verdicts, project
  locks, or successor authorization;
- confirm that Phase 4an does not authorize Phase 4ao or any other
  successor phase;
- and produce the closeout artefact required by the operator convention
  for every phase branch prior to merge.

This closeout does NOT and is NOT authorized to: rerun any historical
strategy or research script; run any backtest; compute any MFE / MAE /
realized-R / cost-decomposition distribution; acquire any data; modify any
data, manifest, source file, test, or script; revise any retained verdict;
modify any project lock; reopen any cooled-down family; reopen the 5m
research thread; modify the M0 governance document
(`docs/00-meta/m0-mechanism-admissibility-gate.md`); modify the Phase 4ak
twelve-clause M0 gate, post-null cooldown rule, or cooled-down families
list; authorize Phase 4ao, Phase 5, Phase 4 canonical, paper / shadow,
live-readiness, deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, public-endpoint calls in code, user
stream, WebSocket, listenKey, MCP, Graphify, `.mcp.json`, or credentials;
or authorize 5m / 1m / aggTrades / tick-data acquisition.

## 6. Inventory Result

The Phase 4an inventory examined ten historical strategy / research
populations plus the closed 5m thread. The artefact-availability
classification is:

- **H0, R3, R1a, R1b-narrow, R2 — `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS`.**
  Local trade-log artefacts (gitignored under `data/derived/backtests/`)
  contain `mfe_r` and `mae_r` populated from 15m bar excursion via
  `src/prometheus/strategy/v1_breakout/management.py::TradeManagement._update_excursions`,
  plus all entry / exit prices and timestamps, fees, slippage cost cell,
  funding PnL, gross / net PnL, realized R, initial stop, and exit-reason
  fields. Per-cost-cell variants (LOW / MEDIUM / HIGH) and trade-price
  stop-domain variants exist for retained-evidence runs. No rerun is
  required for first-pass MFE / MAE / realized-R / cost-decomposition
  forensics.

- **F1, D1-A — `RECONSTRUCTABLE_ONLY_WITH_RERUN` for MFE / MAE;
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` for non-excursion fields.**
  Local `trade_log_v1` artefacts have schema parity with V1-arc and all
  realized-R / cost / timing / exit-reason fields populated, but `mfe_r`
  and `mae_r` are uniformly `0.0` because the F1
  (`src/prometheus/strategy/mean_reversion_overextension/`) and D1-A
  (`src/prometheus/strategy/funding_aware_directional/`) strategy modules
  contain no excursion-tracking code; the engine returns `0.0` defaults
  when `active.management is None`
  (`src/prometheus/research/backtest/engine.py:1139–1140`). Recovery of
  MFE / MAE on F1 / D1-A would require either a controlled rerun under
  script modification or an offline 15m-join over each trade's
  `entry_fill_time_ms` → `exit_fill_time_ms` window using the existing
  v002 BTCUSDT / ETHUSDT 15m bars; neither route is authorized by
  Phase 4an.

- **V2, G1, C1 — `RECONSTRUCTABLE_ONLY_WITH_RERUN`.** The standalone
  research scripts emit aggregate variant-level CSVs only under
  `data/research/phase4l/`, `data/research/phase4r/`, and
  `data/research/phase4x/`. No per-trade ledger is persisted. V2 in-memory
  tracks `mfe_R` (using 30m bar high / low at
  `scripts/phase4l_v2_backtest.py:1224–1226`) but does not persist it
  per-trade and does not track MAE; G1 and C1 do not track MFE / MAE in
  memory at all. Reconstruction of any per-trade forensics requires rerun
  under script modification, which is governance-bounded by Phase 4z /
  Phase 4m / Phase 4s / Phase 4y forbidden-rescue lists and is NOT
  authorized by Phase 4an.

- **5m research thread — `CLOSED_CONTEXT_ONLY`.** The 5m thread (Phases
  3o → 3p → 3q → 3r → 3s → 3t) was diagnostic-only (Q1–Q7) and never
  produced a strategy trade ledger. Phase 3t is operationally CLOSED;
  Phase 4al §14 explicitly says the 5m research thread is not reopened
  by lower-timeframe data-resolution discussion. Phase 4an does not
  reopen it.

Forbidden-rescue-risk profile (under Phase 4al §9 refined no-rescue rule
and the cumulative Phase 4z / Phase 4m / Phase 4s / Phase 4y forbidden-
rescue lists):

- **MEDIUM**: H0, R3 (framework-anchor / baseline-of-record reframings).
- **HIGH**: R1a, R1b-narrow (per-bar bolt-on filter rescue scaffold).
- **CRITICAL**: R2 (no §11.6 relaxation; no R2-prime); F1 (no F1-prime / no
  profitable-subset extraction / no F1 hybrid); D1-A (no D1-A-prime / D1-B
  / V1-D1 / F1-D1 hybrid / no Phase 3s Q6 finding as rule input); V2 (no
  V2-prime / V2-narrow / V2-relaxed / V2 hybrid / no stop-distance
  widening / no setup-window amendment); G1 (no G1-prime / G1-narrow /
  G1-extension / G1 hybrid / no classifier relaxation / no
  K_confirm/ATR-band/V_liq_min/funding-band/E_min amendment); C1 (no
  C1-prime / C1-narrow / C1-extension / C1 hybrid / no volume / funding /
  HTF / mark-price overlay / no threshold tuning); 5m thread (no
  reopening of the 5m strategy thread; no Q1–Q7 outputs as rule-input
  candidates).

Mark-price path forensics is BLOCKED under §1.7.3 stop-trigger-domain
governance and Phase 3v §8; Phase 3s Q6 D1-A finding remains descriptive
only.

Lower-timeframe sufficiency for first-pass forensics: 15m / 30m / 1h / 4h
is sufficient for V1-arc and (via offline reconstruction or rerun) for F1
/ D1-A; 5m would be optional only if intra-bar sequencing ambiguity is
exposed (Phase 4al §14 hierarchy); 1m would only escalate if 5m exceeds
the Phase 4al §14.C >10% / >20% bands; aggTrades / tick remains final
escalation. No lower-timeframe data is acquired by Phase 4an.

Open questions recorded but not answered:

- **OQ-A**: whether offline 15m-join MFE / MAE recovery on F1 / D1-A
  retains useful resolution.
- **OQ-B**: whether V2 / G1 / C1 rerun-based per-trade forensics can
  satisfy the M0 post-null cooldown rule.
- **OQ-C**: whether cross-population realized-R comparisons require a
  Phase 4am §11.A.10-driven methodology-harmonization spec first.
- **OQ-D**: minimum-sufficient predeclared-methodology template that
  satisfies Phase 4al §9.C and the Phase 4ak twelve-clause M0 gate.
- **OQ-E**: forensic-measurement-layer vs reopened-thread boundary for the
  5m research thread.

## 7. Files Added / Modified (Phase 4an, including this closeout)

Added by Phase 4an memo commit `241d6a7`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`
  (1189 lines added).

Modified by Phase 4an memo commit `241d6a7`:

- `docs/00-meta/current-project-state.md`
  (180 lines added — Phase 4an narrative paragraph + new "Current phase:"
  block, with the prior Phase 4am block preserved as historical context).

Added by Phase 4an closeout commit (this file):

- `docs/00-meta/implementation-reports/2026-05-06_phase-4an_closeout.md`.

## 8. Files Not Modified

Phase 4an did NOT modify:

- any source file under `src/prometheus/`;
- any test under `tests/`;
- any script under `scripts/` (including `phase2*.py`,
  `phase3d_F1_execution.py`, `phase3j_D1A_execution.py`,
  `phase3q_5m_acquisition.py`, `phase3s_5m_diagnostics.py`,
  `phase4i_v2_acquisition.py`, `phase4l_v2_backtest.py`,
  `phase4r_g1_backtest.py`, `phase4x_c1_backtest.py`,
  `phase4ac_alt_symbol_acquisition.py`,
  `phase4ae_alt_symbol_substrate_feasibility.py`,
  `phase4af_alt_symbol_regime_persistence.py`,
  `phase4ai_single_position_cross_sectional_trend.py`);
- any data file under `data/raw/`, `data/normalized/`, `data/derived/`,
  or `data/research/`;
- any manifest under `data/manifests/`;
- any strategy specification under `docs/03-strategy-research/`;
- any validation document under `docs/05-backtesting-validation/`;
- any roadmap document under `docs/12-roadmap/` (phase-gates,
  technical-debt-register);
- any governance document under `docs/00-meta/`
  (`m0-mechanism-admissibility-gate.md`, `ai-coding-handoff.md`,
  `implementation-ambiguity-log.md`);
- any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1,
  5m thread);
- any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w);
- any successor authorization.

## 9. Docs-Only Confirmation

Phase 4an is **docs-only**. The phase modifies only Markdown files under
`docs/00-meta/`. No code, tests, scripts, data, manifests, strategy specs,
or governance documents are modified by Phase 4an.

The Phase 4an closeout (this file) is also docs-only and modifies only
this Markdown file under `docs/00-meta/implementation-reports/`.

## 10. Verification Commands and Outputs

Verification commands run on branch
`phase-4an/historical-trade-population-exit-path-inventory` immediately
prior to staging and committing this closeout file:

```text
git status                   : clean working tree (untracked
                                .claude/scheduled_tasks.lock and
                                data/research/ are gitignored / transient)
git branch --show-current    : phase-4an/historical-trade-population-exit-path-inventory
git rev-parse main           : dfaa26a4e7f9a21957e0e465c7bb7de2e508a784
git rev-parse origin/main    : dfaa26a4e7f9a21957e0e465c7bb7de2e508a784
git rev-parse HEAD           : 241d6a71bec61457a8b876572989d7550a9f1423
git log --oneline -8         :
                                241d6a7 docs(phase-4an): inventory historical exit-path artefacts
                                dfaa26a docs(phase-4am): merge merge-closeout
                                23d1f14 docs(phase-4am): add merge closeout
                                9c2c7db docs(phase-4am): merge exit architecture backtest-logic audit
                                6fe3fed docs(phase-4am): audit exit architecture backtest logic
                                f97f850 docs(phase-4al): merge exit architecture M0 admissibility memo
                                8fc7227 docs(phase-4al): exit architecture M0 admissibility memo
                                9abf1bd chore(docs): merge README and current-project-state refresh
git check-ignore data/research/ : .gitignore:88 confirms gitignored
```

After this closeout file is staged and committed, additional verification
commands will be run:

```text
git diff --cached --stat     : (run before commit; will show the new
                                closeout file staged with line count)
git diff --check             : (run before commit; expected clean —
                                no whitespace or merge-conflict markers)
git rev-parse HEAD           : (run after commit; will be the new closeout
                                commit SHA)
git log --oneline -8         : (run after commit; will show the new
                                closeout commit on top of 241d6a7)
```

`ruff` / `pytest` / `mypy` are NOT run because Phase 4an is docs-only with
zero code, test, or script changes — repo convention does not require
quality gates for docs-only phases (consistent with Phase 4al, Phase 4am,
and prior docs-only phases).

## 11. Implementation / Governance Review

### 11.1 What changed?

Phase 4an added one new file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`,
1189 lines) and modified one existing file
(`docs/00-meta/current-project-state.md`, 180 lines added). The Phase 4an
closeout commit additionally adds this file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4an_closeout.md`).

### 11.2 What did not change?

`docs/00-meta/m0-mechanism-admissibility-gate.md` (Phase 4ak durable
governance) is unchanged. All twelve M0 clauses M0.1–M0.12 are unchanged.
The post-null cooldown rule is unchanged. The cooled-down families list is
unchanged. All retained verdicts are unchanged. All project locks are
unchanged. All scripts under `scripts/` are unchanged. All source files
under `src/prometheus/` are unchanged. All tests are unchanged. All data
files are unchanged. All manifests are unchanged.
`docs/12-roadmap/phase-gates.md`,
`docs/12-roadmap/technical-debt-register.md`,
`docs/00-meta/ai-coding-handoff.md`, and
`docs/00-meta/implementation-ambiguity-log.md` are unchanged.

### 11.3 Were any locks, verdicts, or safety boundaries affected?

No. Every retained verdict and every project lock is preserved verbatim.
The Phase 4al refined no-rescue rule, the Phase 4ak twelve-clause M0 gate
+ post-null cooldown rule + cooled-down families list, the Phase 4am
§11.A audit findings (F-1 / F-2 / F-3 / F-4), the Phase 3v §8 stop-trigger-
domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA-slope /
stagnation governance, the Phase 4j §11 metrics OI-subset partial-eligibility
rule, the Phase 4k / Phase 4q / Phase 4w backtest-plan methodologies, and
the Phase 4p / Phase 4v strategy-spec memos are all preserved.

### 11.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 11.5 Is the phase mergeable as docs-only?

Yes. Phase 4an is mergeable as docs-only. The only files added or modified
are the new memo, the new closeout (this file), and the narrow paragraph
addition to `docs/00-meta/current-project-state.md`.

## 12. Research Interpretation Review

### 12.1 What did this phase prove?

Phase 4an proved, by static repository inspection only, that:

- V1-arc populations (H0, R3, R1a, R1b-narrow, R2) have locally-present
  `trade_log_v1` artefacts with `mfe_r` / `mae_r` already populated from
  15m bar excursion, plus all realized-R / cost / timing / exit-reason
  fields, and per-cost-cell variants — sufficient for first-pass
  descriptive forensics WITHOUT rerun;
- F1 and D1-A have schema-parity `trade_log_v1` artefacts with all
  non-excursion fields populated, but `mfe_r` / `mae_r` are uniformly
  zero because the F1 / D1-A strategy modules contain no excursion
  tracker — MFE / MAE forensics on F1 / D1-A would require either rerun
  with excursion instrumentation OR offline 15m-join reconstruction;
- V2, G1, C1 standalone research scripts emit aggregate variant-level
  CSVs only and persist no per-trade ledger — per-trade forensics on
  these populations requires rerun under script modification, and is
  governance-bounded by Phase 4z / Phase 4m / Phase 4s / Phase 4y
  forbidden-rescue lists;
- the 5m research thread is closed historical context only and is not
  reopened by Phase 4an;
- every population carries a forbidden-rescue-risk profile (MEDIUM for
  H0 / R3; HIGH for R1a / R1b-narrow; CRITICAL for R2 / F1 / D1-A / V2 /
  G1 / C1 / 5m thread).

### 12.2 What did this phase not prove?

Phase 4an did NOT prove:

- the actual distributions of MFE / MAE / realized-R / cost across any
  population (no computation done);
- whether any population's path patterns are interesting or boring;
- whether the V1-arc cost-decomposition is methodologically harmonized
  with V2 / G1 / C1 cost-decomposition (this is OQ-C);
- whether 5m-resolution forensics on F1 / D1-A would expose meaningful
  intra-bar sequencing (this is OQ-A);
- whether V2 / G1 / C1 rerun under script modification is admissible at
  all under the M0 post-null cooldown rule (this is OQ-B);
- which populations are most worth analyzing first.

### 12.3 Which original questions did it answer?

- Q1: which populations have sufficient artefacts → V1-arc immediately;
  F1 / D1-A non-excursion fields immediately, MFE / MAE only via rerun
  or offline 15m-join; V2 / G1 / C1 only via rerun.
- Q2: which require lower-timeframe data → none for first-pass; 5m
  optional only under Phase 4al §14 if a forensic question exposes
  intra-bar ambiguity.
- Q3: which require reruns → V2 / G1 / C1 (any per-trade); F1 / D1-A
  (MFE / MAE only).
- Q4: which are governance-blocked for rescue use → all ten populations
  carry forbidden-rescue-risk; HIGH for R1a / R1b-narrow; CRITICAL for
  R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread.
- Q5: clean next step → remain paused.

### 12.4 Which original questions remain open?

OQ-A through OQ-E above (§6).

### 12.5 What does it mean for strategy research?

It means that the historical strategy-research record now has a clear
inventory of what could be examined later if any future forensic phase
were ever authorized. It does NOT mean any strategy research is unblocked.
The M0 cooled-down families list still cools down price-only single-symbol
directional continuation (DEPLETED), cross-sectional trend / relative-
strength symbol selection under Phase 4ai descriptors
(COOLED_DOWN_AFTER_NOT_SUPPORTED), derivatives-context directional
(CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK), microstructure / order-flow
(NOT_RECOMMENDED_NOW), mark-price stop-domain (NOT_RECOMMENDED_NOW).
Phase 4an does not update that list.

### 12.6 What does it mean for governance?

It means that any future forensic phase has a defensible map of what
artefacts exist and what would require rerun, and that the forbidden-
rescue-risk profile of every population is documented in advance of any
computation. The methodology-harmonization gap (V2 cost-application
DOCUMENTATION_LIMITATION; F1 / D1-A missing MFE / MAE; V2 / G1 / C1
missing per-trade ledger) is now explicit. Future forensic work would
benefit from a methodology-harmonization memo BEFORE any computation.

### 12.7 What is the clean next step?

Remain paused. The inventory is complete; no forensic computation is
required to proceed; no successor phase is authorized.

### 12.8 What should we not do yet?

Do not start any forensic phase. Do not rerun V2 / G1 / C1. Do not rerun
F1 / D1-A. Do not compute offline MFE / MAE joins. Do not acquire 5m / 1m /
aggTrades / tick. Do not reopen the 5m research thread. Do not propose a
new strategy. Do not authorize Phase 4ao / Phase 5 / Phase 4 canonical /
paper / shadow / live / exchange-write / production keys / authenticated
APIs / private endpoints / user stream / WebSocket / MCP / Graphify /
`.mcp.json` / credentials. Do not modify the M0 governance document. Do
not modify any retained verdict. Do not modify any project lock.

## 13. Preserved Verdicts and Locks

### 13.1 Retained verdicts (preserved verbatim)

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6 cost-sensitivity blocks.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- 5m research thread remains operationally CLOSED per Phase 3t.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

### 13.2 Project locks (preserved verbatim)

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- §11.6 HIGH cost remains 8 bps per side (round-trip = 16 bps slippage)
  unless a later separately authorized methodology distinguishes
  fee / slippage components without changing the project lock.
- §1.7.3 project-level locks remain:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance
  preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved.
- Phase 4k V2 backtest-plan methodology preserved.
- Phase 4p G1 strategy-spec memo preserved.
- Phase 4q G1 backtest-plan methodology preserved.
- Phase 4v C1 strategy-spec memo preserved.
- Phase 4w C1 backtest-plan methodology preserved.
- Phase 4ak twelve-clause M0 mechanism-admissibility gate preserved.
- Phase 4ak post-null cooldown rule preserved.
- Phase 4ak cooled-down families list preserved.
- Phase 4al refined no-rescue rule preserved.
- Phase 4al §13 future-Phase-4am-style boundary specification preserved.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved as
  documentation for future methodology-harmonization scoping.

### 13.3 No-rescue constraints (preserved verbatim)

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid.
- No conversion of Phase 4an inventory findings into strategy candidates.
- No conversion of Phase 4an forbidden-rescue-risk classifications into
  parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4an findings.
- No verdict revision.
- No project-lock revision.

## 14. Recommendation

- **Primary**: remain paused. The Phase 4an inventory is on record; no
  computation is required to proceed; no successor phase is authorized.
- **Conditional secondary (NOT authorized by Phase 4an)**: a narrower
  future docs-only methodology / artefact harmonization memo if separately
  authorized. Resolves OQ-C / OQ-D before any computation; does NOT itself
  authorize computation.
- **Conditional tertiary (NOT authorized by Phase 4an)**: a future full
  exit-path forensic plan only after harmonization, restricted to V1-arc
  populations under Phase 4al §13 boundaries. F1 / D1-A computation, if
  ever authorized, prefers the offline-15m-join route on rescue-risk
  grounds. V2 / G1 / C1 computation is prima facie governance-blocked by
  the M0 post-null cooldown rule.
- **Not recommended**: starting forensic work without harmonization;
  treating Phase 4an artefact-availability findings as authorization to
  analyze; using forbidden-rescue-risk classifications as a population-
  ranking scheme.
- **Forbidden**: paper / shadow / live / exchange-write / production
  keys / authenticated APIs / private endpoints / user stream / WebSocket /
  MCP / Graphify / `.mcp.json` / credentials; any strategy resurrection;
  any verdict revision; any project-lock revision; any M0-governance
  amendment derived from Phase 4an findings; reopening the 5m research
  thread.

**Phase 4an does not authorize any successor phase.**

## 15. Final Status

- Phase 4an is complete on the phase branch
  `phase-4an/historical-trade-population-exit-path-inventory`.
- Phase 4an is docs-only.
- Phase 4an memo commit on the phase branch:
  `241d6a71bec61457a8b876572989d7550a9f1423`.
- Phase 4an closeout commit on the phase branch: recorded after this file
  is staged and committed.
- Phase 4an is ready for no-fast-forward merge to main after the closeout
  commit lands on the phase branch.
- The merge-closeout file
  `docs/00-meta/implementation-reports/2026-05-06_phase-4an_merge-closeout.md`
  will be created during the no-fast-forward merge per operator convention.
- **No successor phase is authorized.**
- **Phase 4ao / Phase 5 / Phase 4 canonical / any successor phase remains
  unauthorized.**
- **Paper / shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in code,
  user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials,
  exchange-write, and 5m / 1m / aggTrades / tick-data acquisition all
  remain unauthorized.**
- **Recommended state remains paused** unless the operator separately
  authorizes a future phase.
