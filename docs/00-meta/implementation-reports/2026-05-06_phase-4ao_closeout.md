# Phase 4ao Closeout — Exit-Path Methodology / Artefact Harmonization Memo

## 1. Phase Identity

- Name: Phase 4ao — Exit-Path Methodology / Artefact Harmonization Memo.
- Type: docs-only methodology / artefact harmonization / closeout.
- Date: 2026-05-06.
- Phase memo: `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`.

## 2. Branch

- Phase branch: `phase-4ao/exit-path-methodology-artefact-harmonization`.
- Forked from: clean main at `a73c00b1de878ca9ee020a7942bd9af7ebb831ed`
  (the live Phase 4an merge tip on main / origin/main).

## 3. Base SHA

- Pre-Phase-4ao main / origin/main: `a73c00b1de878ca9ee020a7942bd9af7ebb831ed`.
- Note: the Phase 4an merge-closeout file at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4an_merge-closeout.md`
  records merge commit SHA `bf3643c5e6b04255e6ed19a074526332d5f35a5c` per
  the documented git self-reference artifact (every amend produces a new
  SHA, so the recorded SHA is one amend cycle behind the live HEAD). The
  live Phase 4an merge tip on main is `a73c00b`. Both SHAs are part of
  the amend chain; only `a73c00b` is in main's live history.

## 4. Phase Commit SHAs

- Phase 4ao memo + current-project-state commit:
  `6ace04fa6abb69e2ce7eb716c402bb7738ccedce`
  ("docs(phase-4ao): harmonize exit-path methodology").
- Phase 4ao closeout commit: recorded after this file is staged and
  committed.

## 5. Purpose

Phase 4ao is a docs-only methodology / artefact harmonization memo that
defines how any future exit-path forensic phase would have to be specified
before computation. It is derived from the Phase 4an inventory baseline
and converts that inventory into a usable per-population forensic
methodology specification, without performing any forensic analysis,
without computing any distribution, without running any script, without
acquiring any data, without modifying any data / manifest / source / test /
script / strategy parameter / threshold / project lock / retained
verdict / M0 governance, and without authorizing any successor phase.

This closeout file is the Phase 4ao closeout per the operator phase-
branch convention. Its purpose is to:

- close out Phase 4ao on the phase branch before any future no-fast-
  forward merge to main;
- record the harmonization result in summary form for repository-level
  governance review;
- preserve the retained verdict ledger and every project lock verbatim;
- confirm that Phase 4ao did not modify source / tests / scripts / data /
  manifests / strategy specs / governance docs / retained verdicts /
  project locks / successor authorization;
- confirm that Phase 4ao does not authorize Phase 4ap or any other
  successor phase;
- and produce the closeout artefact required by the operator convention
  for every phase branch prior to merge.

## 6. Harmonization Result

Phase 4ao defined six headline harmonization rules:

1. **Population scope for any future first-pass forensic phase**:
   V1-arc only (H0 / R3 / R1a / R1b-narrow / R2). R3 is included as
   baseline-of-record for descriptive context and explicitly NOT as an
   optimization target (no R3-prime / R3 next-spec / R3 baseline-of-
   record revision). F1 / D1-A may be admissible later via a strict
   offline 15m-join Route B reconstruction under separate authorization
   (Route B preferred over Route A controlled-rerun on rescue-risk
   grounds because Route B does not modify or re-execute strategy code).
   V2 / G1 / C1 rerun-based per-trade forensics is conservatively
   classified as **governance-risk-unresolved** under the M0 post-null
   cooldown rule and is not recommended for first-pass forensics until
   a separately authorized OQ-B-resolution memo clarifies the
   admissibility.

2. **MFE / MAE definition harmonization**:
   - V1-arc and F1 / D1-A: 15m bar-extreme based.
   - V2: 30m bar-extreme based; in-memory only; not persisted; no MAE.
   - G1 / C1: not tracked.
   - 5m: measurement-layer escalation only when ambiguity threshold
     exposed (Phase 4al §14 hierarchy / §14.C bands).
   - 1m and tick / aggTrades: final escalation; remain unauthorized.
   - Bar-resolution caveats explicitly recorded.
   - Single-bar trades: entry-bar high / low envelope (not zero by
     default).
   - No-trade / zero-qualifying-trade populations: no per-trade
     forensic content.

3. **Realized-R / cost-field harmonization across seven axes**:
   1. Engine path (V1-arc / F1 / D1-A backtest engine vs V2 / G1 / C1
      standalone-script accounting).
   2. Fee assumption (V1-arc / F1 / D1-A `fee_rate_assumption = 0.0005`
      = 5 bps / side; V2 / G1 / C1 `TAKER_FEE_PER_SIDE_BPS = 4` per side;
      both research-conventions; §11.6 LOCK is 8 bps slippage / side, NOT
      the fee).
   3. Slippage cell (LOW / MEDIUM / HIGH per side; HIGH = 8 bps / side
      preserved verbatim per §11.6).
   4. Funding handling (V2 right-inclusive `(entry_ms, exit_ms]`; G1
      strictly between `(entry_ms, exit_ms)`; C1 excluded per Phase 4w).
   5. Cost-cell label.
   6. Stop-trigger-domain label (Phase 3v §8).
   7. Per-trade vs aggregate.
   §11.6 is preserved verbatim; future fee / slippage / funding
   decomposition is descriptive only.

4. **Stop-trigger-domain governance (Phase 3v §8)**: preserved.
   `trade_price_backtest`, `mark_price_runtime`,
   `mark_price_backtest_candidate` remain valid. `mixed_or_unknown`
   fails closed. Mark-price path forensics for live-readiness remains
   BLOCKED under §1.7.3.

5. **5m boundary (Phase 3t closure)**: preserved.
   Existing 5m data may be referenced as a forensic measurement layer
   only under the conservative §13.3 criterion (predeclared bar-
   resolution-ambiguity question; no new 5m strategy or rule; no Q1–Q7
   conversion to rule input; documented in predeclared methodology;
   separately authorized successor phase). The 5m strategy thread is
   NOT reopened. Q1–Q7 outputs are NOT rule-input candidates.

6. **Minimum predeclared-methodology template (§14)**: 18 required
   headings any successor computation phase must include before
   computation begins (population(s) included; population(s) excluded;
   reason for inclusion; artefact source; field definitions; cost
   assumptions; stop-trigger-domain label; timeframe / data-resolution
   label; MFE / MAE definition; bar-ambiguity handling; lower-timeframe
   escalation rule; forbidden interpretations; allowed interpretations;
   no-rescue statement; verdict / lock preservation statement; outputs
   to produce; stop conditions; merge / closeout requirements).

**Open question status after Phase 4ao**:

- **OQ-A** (offline 15m-join MFE / MAE recovery sufficiency for F1 /
  D1-A): unresolved until a separately authorized computation phase.
  Route B preferred over Route A on rescue-risk grounds.
- **OQ-B** (V2 / G1 / C1 rerun under M0): conservatively classified as
  governance-risk-unresolved. Phase 4ao defers to a separately
  authorized OQ-B-resolution memo.
- **OQ-C** (Phase 4am V2 cost-application limitations and cross-
  population realized-R comparisons): answered YES, harmonization spec
  required; seven accounting axes specified per Phase 4ao §11.
- **OQ-D** (minimum-sufficient predeclared-methodology template):
  specified per Phase 4ao §14 with 18 required headings.
- **OQ-E** (forensic-measurement-layer vs reopened-thread boundary for
  5m): conservative criterion specified per Phase 4ao §13.3.

## 7. Files Added / Modified (Phase 4ao, Including This Closeout)

Added by Phase 4ao memo + current-project-state commit `6ace04f`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`
  (1329 lines added).

Modified by the same commit:

- `docs/00-meta/current-project-state.md`
  (152 lines added — Phase 4ao narrative paragraph + new "Current
  phase:" block, with the prior Phase 4an block preserved as historical
  context).

Added by Phase 4ao closeout commit (this file):

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_closeout.md`.

## 8. Files Not Modified

Phase 4ao did NOT modify:

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
- any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1,
  C1, 5m thread);
- any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w);
- any M0 governance text (Phase 4ak twelve-clause M0 gate, post-null
  cooldown rule, cooled-down families list);
- any successor authorization.

## 9. Docs-Only Confirmation

Phase 4ao is **docs-only**. The phase modifies only Markdown files under
`docs/00-meta/`. No code, tests, scripts, data, manifests, strategy
specs, validation thresholds, or governance documents are modified by
Phase 4ao.

The Phase 4ao closeout (this file) is also docs-only and modifies only
this Markdown file under `docs/00-meta/implementation-reports/`.

## 10. Verification Commands and Outputs

Verification commands run on branch
`phase-4ao/exit-path-methodology-artefact-harmonization` immediately
prior to staging and committing this closeout file:

```text
git status                   : clean working tree (untracked
                                .claude/scheduled_tasks.lock and
                                data/research/ are gitignored / transient)
git branch --show-current    : phase-4ao/exit-path-methodology-artefact-harmonization
git rev-parse main           : a73c00b1de878ca9ee020a7942bd9af7ebb831ed
git rev-parse origin/main    : a73c00b1de878ca9ee020a7942bd9af7ebb831ed
git rev-parse HEAD           : 6ace04fa6abb69e2ce7eb716c402bb7738ccedce
git log --oneline -8         :
                                6ace04f docs(phase-4ao): harmonize exit-path methodology
                                a73c00b docs(phase-4an): merge historical exit-path inventory
                                13f519b docs(phase-4an): add closeout
                                241d6a7 docs(phase-4an): inventory historical exit-path artefacts
                                dfaa26a docs(phase-4am): merge merge-closeout
                                23d1f14 docs(phase-4am): add merge closeout
                                9c2c7db docs(phase-4am): merge exit architecture backtest-logic audit
                                6fe3fed docs(phase-4am): audit exit architecture backtest logic
git diff --check (pre-each-commit) : clean (no whitespace errors)
git diff --cached --stat (pre-memo): docs/00-meta/current-project-state.md +152;
                                       phase-4ao memo +1329 (2 files; 1481 insertions)
```

After this closeout file is staged and committed, additional verification
commands will be run:

```text
git diff --cached --stat (pre-closeout) : (this file +N lines)
git diff --check                        : clean
git rev-parse HEAD (post-closeout)      : (the new closeout commit SHA)
git log --oneline -8 (post-closeout)    : (closeout on top of 6ace04f)
```

`ruff` / `pytest` / `mypy` are NOT run because Phase 4ao is docs-only
with zero code, test, or script changes — repo convention does not
require quality gates for docs-only phases (consistent with Phase 4al,
Phase 4am, Phase 4an, and prior docs-only phases).

## 11. Implementation / Governance Review

### 11.1 What changed?

Phase 4ao added one new file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`,
1329 lines) and modified one existing file
(`docs/00-meta/current-project-state.md`, 152 lines added). The Phase
4ao closeout commit additionally adds this file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4ao_closeout.md`).

### 11.2 What did not change?

- `docs/00-meta/m0-mechanism-admissibility-gate.md`: unchanged.
- All twelve M0 clauses M0.1–M0.12: unchanged.
- The post-null cooldown rule: unchanged.
- The cooled-down families list: unchanged.
- All retained verdicts: unchanged.
- All project locks: unchanged.
- All scripts under `scripts/`: unchanged.
- All source files under `src/prometheus/`: unchanged.
- All tests: unchanged.
- All data files: unchanged.
- All manifests: unchanged.
- `docs/12-roadmap/phase-gates.md`,
  `docs/12-roadmap/technical-debt-register.md`,
  `docs/00-meta/ai-coding-handoff.md`,
  `docs/00-meta/implementation-ambiguity-log.md`: unchanged.

### 11.3 Were any locks, verdicts, or safety boundaries affected?

No.

### 11.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 11.5 Is the phase mergeable as docs-only?

Yes. Phase 4ao is mergeable as docs-only. The only files added or
modified are the new memo, the new closeout (this file), and the narrow
paragraph addition + "Current phase:" block update on
`docs/00-meta/current-project-state.md`.

## 12. Research Interpretation Review

### 12.1 What did this phase prove?

Phase 4ao proved, by static repository inspection only, that:

- A single harmonized methodology framework can be defined for any
  future exit-path forensic phase across the ten historical Prometheus
  populations plus the 5m thread context, without revising any retained
  verdict or any project lock.
- V1-arc populations require no rerun and no offline reconstruction for
  first-pass MFE / MAE / realized-R / cost-decomposition forensics.
- F1 / D1-A MFE / MAE forensics requires either Route A (rerun with
  excursion instrumentation) or Route B (offline 15m-join). Route B is
  preferred on rescue-risk grounds.
- V2 / G1 / C1 rerun-based per-trade forensics is governance-risk-
  unresolved under the M0 post-null cooldown rule and should be
  deferred until a separately authorized OQ-B resolution memo
  clarifies whether audit-only rerun is admissible.
- Cross-population realized-R comparison requires explicit accounting
  separation along seven axes; failure to separate these would conflate
  methodologies. §11.6 is preserved verbatim.
- Stop-trigger-domain governance (Phase 3v §8) and 5m closure (Phase
  3t) remain binding.
- A minimum predeclared-methodology template (§14) suffices as the
  precondition for any successor computation phase.

### 12.2 What did this phase not prove?

Phase 4ao did NOT prove:

- the actual distributions of MFE / MAE / realized-R / cost-decomposition
  on any population (no computation done);
- whether offline 15m-join Route B reconstruction recovers useful
  MFE / MAE resolution on F1 / D1-A (this is OQ-A; only authorized
  computation can answer);
- whether the M0 post-null cooldown rule formally permits audit-only
  rerun on V2 / G1 / C1 (this is OQ-B; only a separately authorized
  OQ-B-resolution memo can clarify);
- which V1-arc populations are most worth analyzing first
  (no prioritization done);
- any specific numerical claim about cost-cell sensitivity, regime
  fragility, or path patterns.

### 12.3 Which original questions did it answer?

- **OQ-B**: conservatively classified governance-risk-unresolved; Phase
  4ao defers to a future separately authorized OQ-B-resolution memo.
- **OQ-C**: answered YES, with seven-axis disclaim required.
- **OQ-D**: specified per §14 (18 required headings).
- **OQ-E**: conservative criterion specified per §13.3.

### 12.4 Which original questions remain open?

- **OQ-A**: cannot be answered without authorized computation; Route B
  preferred if ever authorized.
- The M0-formal-status of audit-only rerun on V2 / G1 / C1 remains
  formally unresolved despite Phase 4ao's conservative interpretation
  in §10.

### 12.5 What does it mean for strategy research?

It means that any future exit-path forensic phase has a defensible
methodology, definitional, accounting, and governance map already on
the project record. It does NOT mean that any forensic phase is
unblocked. The M0 cooled-down families list is unchanged.

### 12.6 What does it mean for governance?

It means the methodology-harmonization gap identified in Phase 4an is
now closed at the documentation level. Any successor phase has a
single template (§14) to follow, a single per-population eligibility
matrix (§15), and a single set of cross-population accounting axes
(§11). All upstream governance is preserved verbatim.

### 12.7 What is the clean next step?

Remain paused. The harmonization is on record; no successor phase is
authorized.

### 12.8 What should we not do yet?

Do not start any forensic computation. Do not rerun any strategy
script. Do not run an offline join. Do not modify any strategy or
backtest code. Do not acquire 5m / 1m / aggTrades / tick / mark-price
30m / 4h data. Do not reopen the 5m research thread. Do not propose a
new strategy. Do not authorize Phase 4ap / Phase 5 / Phase 4 canonical /
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
- §11.6 HIGH cost remains preserved (8 bps slippage per side; round-trip
  = 16 bps). Any future fee / slippage / funding decomposition may be
  reported descriptively only and must not change the locked project-
  level cost reference or revise historical results.
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
- Phase 4al §13 boundary specification preserved.
- Phase 4al §14 data-resolution hierarchy preserved.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved.
- Phase 4an inventory result preserved.

### 13.3 No-rescue constraints (preserved verbatim)

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid.
- No conversion of Phase 4ao methodology / harmonization findings into
  strategy candidates.
- No conversion of Phase 4ao forbidden-rescue-risk classifications into
  parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4ao reasoning.
- No verdict revision.
- No project-lock revision.

## 14. Recommendation

- **Primary**: remain paused. The Phase 4ao harmonization is on record;
  no computation is required to proceed; no successor phase is
  authorized.
- **Conditional secondary (NOT authorized by Phase 4ao)**: future
  docs-only V1-arc-only exit-path forensic plan. R3 included as
  baseline-of-record for descriptive context only (no R3 optimization,
  R3-prime, R3 rescue, or baseline-of-record revision). Methodology
  must satisfy the §14 18-heading template verbatim.
- **Conditional tertiary (NOT authorized by Phase 4ao)**: future
  docs-only OQ-B resolution memo addressing V2 / G1 / C1 rerun
  admissibility under the M0 post-null cooldown rule.
- **Conditional quaternary (NOT authorized by Phase 4ao)**: future
  docs-only F1 / D1-A Route B reconstruction methodology memo (offline
  15m-join; standalone-script boundary; predeclared outputs).
- **Not recommended**: starting forensic computation without §14
  predeclared methodology; treating Phase 4ao allowed-uses lists as
  authorization to compute; using forbidden-rescue-risk classifications
  as a population-ranking scheme; combining secondary / tertiary /
  quaternary into a single successor phase.
- **Forbidden**: paper / shadow / live / exchange-write / production
  keys / authenticated APIs / private endpoints / user stream /
  WebSocket / MCP / Graphify / `.mcp.json` / credentials; any strategy
  resurrection; any verdict revision; any project-lock revision; any
  M0-governance amendment derived from Phase 4ao reasoning; reopening
  the 5m research thread; acquisition of 5m / 1m / aggTrades / tick /
  mark-price 30m / 4h data without separately authorized data-
  requirements memo.

**Phase 4ao does not authorize any successor phase.**

## 15. Final Status

- Phase 4ao is complete on the phase branch
  `phase-4ao/exit-path-methodology-artefact-harmonization`.
- Phase 4ao is docs-only.
- Phase 4ao memo + current-project-state commit on the phase branch:
  `6ace04fa6abb69e2ce7eb716c402bb7738ccedce`.
- Phase 4ao closeout commit on the phase branch: recorded after this
  file is staged and committed.
- Phase 4ao is ready for no-fast-forward merge to main after the
  closeout commit lands on the phase branch (operator-driven; not
  performed in this prompt).
- The merge-closeout file
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_merge-closeout.md`
  will be created during the no-fast-forward merge per operator
  convention if and when the operator authorizes the merge.
- **No successor phase is authorized.**
- **Phase 4ap / Phase 5 / Phase 4 canonical / any successor phase
  remains unauthorized.**
- **Paper / shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in code,
  user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials,
  exchange-write, and 5m / 1m / aggTrades / tick / mark-price 30m / 4h
  data acquisition all remain unauthorized.**
- **Recommended state remains paused** unless the operator separately
  authorizes a future phase.
