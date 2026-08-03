# Phase 4bn-BC — CF-1 Valid-Pass Filter-Admissibility and Consequence Assessment

## 1. Phase identity

Phase 4bn-BC — CF-1 Valid-Pass Filter-Admissibility and Consequence Assessment. A **docs-only
decision and governance** phase that makes exactly one primary decision about the consequence of the
merged Phase 4bn-BB `CF1_VALID_PASS`, plus one separate evidence-governance decision. It is the
docs-only decision phase that the Phase 4bn-AX §14 and Phase 4bn-AY §31 predeclared pass consequence
permits — and only permits — after a valid CF-1 pass.

This phase decides a **consequence**. It does not design, specify, parameterize, implement, or run
any filter, and it does not recompute, reinterpret, or extend any Phase 4bn-BB value.

`Phase 4bn-BB remains CF1_VALID_PASS and its single evidence-bearing run remains consumed.`

## 2. Branch, base, and lineage SHAs

- **Branch:** `phase-4bn-bc/cf1-valid-pass-filter-admissibility-consequence-assessment`.

| Item | SHA |
|---|---|
| Base `main` == `origin/main` == `HEAD` at branch creation (Phase 4bn-BB merge-closeout SHA-finalization tip) | `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49` |
| Phase 4bn-BB no-fast-forward merge commit | `0200d576884ae8461f75768b97b8ad9d938a8a9b` |
| Phase 4bn-BB merge-closeout branch commit | `4214c658fea625be1d626af99324c5c0babea57c` |
| Phase 4bn-BB pre-merge closeout / final source-branch tip | `345165710ddb17622d6c679e2d350f2779022068` |
| Phase 4bn-BB result (execution + verdict + artefact/leakage) commit | `6ba76b56a514cb0abaeac0480a59a688a7cdebeb` |
| Phase 4bn-BB implementation commit | `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917` |
| Phase 4bn-BA merge-closeout SHA-finalization tip / Phase 4bn-BB base | `e26193e8f61cae797e4cbfab932025b709b74566` |

Base state verified in sync before any mutation. The only untracked item throughout was the transient
`.claude/scheduled_tasks.lock`, which was never staged, modified, deleted, cleaned, or committed.

## 3. Phase type and risk tier

**Phase type.** Docs-only decision and governance assessment. No data; no model; no metric
recomputation; no filter implementation; no filter execution; no reserve-spend authorization; no
strategy / PnL / backtest authorization. It reads committed documentation, committed source and tests
where needed to understand capability boundaries, and Git metadata, and creates exactly three new
documentation files.

**Risk tier.** Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`. It
decides the downstream consequence of the project's only positive scientific result and therefore
bears on scientific direction and downstream authorization, so it takes the highest ceremony tier
even though it mutates no eligibility, manifest, verdict, reserve, ledger, or lock.

## 4. Exact authorization boundary

**Authorized:** read committed docs, committed source and tests, and Git metadata read-only; reason
statically and symbolically over committed governance; author exactly three new documentation files;
commit and push the dedicated phase branch.

**Not authorized:** to open, read, list-for-content, sample, parse, hash, or score anything under
`data/microstructure/` or `data/research/`; to inspect the Phase 4bn-BB v002 local artefact root or
the Phase 4bn-AZ v001 local artefact root; to open any Parquet, local research JSON, or sidecar; to
recompute QLIKE, the bootstrap, or any condition number; to fit a model; to generate any target or
feature; to run the Phase 4bn-BB runner in `--preflight` or `--run` form; to run any project script,
builder, diagnostic, backtest, replay, or runtime process; to run pytest, Ruff, or mypy; to use
network, web, API, or Binance endpoints; to use credentials, `.env`, WebSocket, MCP, Graphify, or
`.mcp.json`; to use Fable or any other external reviewer; to modify, delete, or rename any existing
file; to create source, tests, scripts, configs, manifests, ledgers, process standards, phase gates,
technical-debt entries, reserve proposals, or successor prompts; to open or spend any evidence
reserve; or to authorize any successor phase.

This phase is **static repository reasoning only**. No scientific value is newly computed from any
evidence-bearing data.

## 5. Documents inspected

Committed, read-only. `README` and `docs/00-meta/current-project-state.md` are treated as
navigational and potentially stale; recent implementation reports, merge-closeouts, binding
governance documents, committed source, committed tests, and Git history outrank them.

**Phase 4bn-BB (complete scientific evidence for this phase):**

- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-execution-and-verdict.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-artefact-leakage-and-split-validation.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_closeout.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_merge-closeout.md`

**Phase 4bn-BA (corrected contract lineage):**

- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md`
- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-estimability-and-anti-duplication-audit.md`
- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-corrected-execution-validation-checklist.md`

**CF-1 selection / consequence lineage:**

- `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit.md`
- `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_forced-flow-overlap-proxy-validity-and-m0-audit.md`
- `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-realized-volatility-substrate-test-preregistration.md`
- `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md`

**Stopped-arc lineage:**

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md`
- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md`

**Binding governance:**

- `docs/00-meta/m0-mechanism-admissibility-gate.md` (twelve clauses; §6 cooldown; §7 cooled-down
  families)
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (especially §19)
- `docs/00-meta/process/evidence-budget-ledger.md`
- `docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md`
- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-consequence-protocol.md`
  and its closeout / merge-closeout
- Phase 4bn-Y chronological split / holdout policy as restated through the ledger and the Phase
  4bn-AY §20/§21 development-evidence boundary
- `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`

**Process standards under `docs/00-meta/process/`:** `phase-workflow-standard.md`,
`phase-risk-tiering-standard.md`, `operator-report-standard.md`, `merge-closeout-standard.md`,
`phase-prompt-template.md`, `claude-code-context-management-standard.md`,
`claude-code-lightweight-workspace-standard.md`.

## 6. No-data / no-execution statement

Confirmed. Nothing under `data/microstructure/` or `data/research/` was opened, read, listed for
content, sampled, parsed, hashed, or scored. The Phase 4bn-BB v002 local artefact root
(`data/research/cf1_corrected_realized_volatility_substrate_test_v002/`) and the Phase 4bn-AZ v001
local artefact root (`data/research/cf1_realized_volatility_substrate_test_v001/`) were not
inspected. No Parquet, no local research JSON, and no sidecar was opened. No QLIKE value, bootstrap
replicate, or condition number was recomputed. No model was fitted; no target or feature was
generated. The Phase 4bn-BB runner was not invoked in any mode. No project script, builder,
diagnostic, backtest, replay, or runtime process was run. `pytest`, Ruff, and mypy were not run. No
network, web, API, or Binance endpoint was used; no credential, `.env`, WebSocket, MCP, Graphify, or
`.mcp.json` was used; no external reviewer was used. **No row-level prediction was inspected.**

Every scientific value in this memo is transcribed verbatim from the committed Phase 4bn-BB reports.

## 7. Exact Phase 4bn-BB outcome and merged result state

Scientific outcome:

```
CF1_VALID_PASS
```

Exact merged result state on `main`:

```
CF1_CORRECTED_VALID_PASS_MERGED_TO_MAIN__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__NO_RERUN_AUTHORIZED__DOCS_ONLY_FILTER_ASSESSMENT_REQUIRED_BEFORE_ANY_DOWNSTREAM_ACTION__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

## 8. Exact evidence summary (transcribed, not recomputed)

**Corrected feature pair (frozen, canonical order):**

```
CORRECTED_CF1_FEATURE_SET   = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
```

**Prohibited feature:** `rolling_quantity_mean_60s`.

**Origins:** candidate 5,854; valid paired 5,516; invalid 338 (`har_unavailable` 336,
`har_coverage_failure` 2); zero-RV origins 0.

**Per-block loss differentials `D_i` (baseline − augmented):**

| Block | `D_i` |
|---|---|
| B1 | +2.801856e-03 |
| B2 | +2.152699e-02 |
| B3 | +1.520265e-02 |
| B4 | +2.492981e-03 |
| B5 | +1.422829e-02 |
| B6 | +8.644941e-03 |
| B7 | +1.867419e-02 |

All seven are positive.

**Equal-weighted QLIKE:** baseline `0.32573980348957254`; augmented `0.31380095965814664`.

**Primary improvement:** `Δ_equal = 0.011938843831425896`.

**Descriptive relative improvement:** `ρ = 0.036651473671709504`.

**Bootstrap:** 10,000 replicates; NumPy `PCG64`; seed `20260715`; one-sided 95% lower percentile;
`LB_95 = 0.006273843055395148`.

**Pass state:** `P1 = true`; `P2 = true` (7/7); `P3 = true`; validity `= true`.

**Numerical state:** baseline rank 4/4 in all seven blocks; augmented rank 6/6 in all seven blocks;
augmented condition numbers approximately `3.983e2` through `6.494e2`; the frozen invalidation
threshold remains `> 1e10`.

**Exact Phase 4bn-BB scientific consequence (unchanged):** the valid pass supports development-level
incremental one-hour realized-volatility magnitude information only. It establishes no direction, no
signal, no strategy, no profitability, no economic materiality, no transaction-cost clearance, no
ability to clear 8 bps/side or 16 bps round trip, no tradability, no M0 clearance, no terminal-reserve
confirmation, and no sealed-test confirmation.

## 9. Original Phase 4bn-AX / Phase 4bn-AY predeclared pass consequence

The pass consequence was predeclared **narrowly**, before any data existed, in Phase 4bn-AX §14 and
restated verbatim in substance in Phase 4bn-AY §31:

- record the admissible aggTrades substrate as **scientifically informative on the magnitude axis**;
- authorize **nothing** automatically;
- permit **only** a separately-authorized docs-only decision phase **assessing whether** the forecast
  **could** support a bounded, non-directional market-state / volatility-regime filter;
- do **not** infer direction; do **not** infer profitability; do **not** claim ability to clear 16 bps;
- do **not** authorize position sizing, trade gating, execution timing, PnL analysis, paper / shadow /
  live trading, terminal evidence, or sealed evidence;
- do **not** reopen `STOP_LONGHORIZON_ML_ARC`;
- a development-level pass is **not** reserve-confirmed evidence.

Two features of that predeclaration govern this phase and are decisive below.

First, the permitted continuation is an **assessment of whether**, not a preregistration. The
predeclared consequence is satisfied by a reasoned negative answer exactly as much as by a positive
one; answering "no" is faithful execution of the preregistration, not deviation from it.

Second, Phase 4bn-AX §17 recorded the momentum-by-success risk explicitly and bounded it as a
**condition of the selection, not an afterthought**: a pass could create pressure to reopen
directional work, to trade on a "confident volatility regime", or to touch reserves, and the pass
authorizes only the assessment.

## 10. Exact definition of a bounded, non-directional filter used by this phase

For Phase 4bn-BC, a **potentially admissible future filter** means only:

> A bounded, non-directional research object that uses the already-defined CF-1 future-volatility
> magnitude forecast to characterize or condition a market-state / volatility-regime **label**.

It is **not a trade filter**. It is explicitly **not**: entry gating; exit gating; position sizing;
leverage selection; long/short selection; trade direction; execution timing; stop placement;
profit-taking; threshold trading; confidence-gated trading; risk-budget allocation; portfolio
allocation; PnL conditioning; transaction-cost optimization; or live risk control.

No such object may be called "tradable", "profitable", "edge", "signal", "risk-on", "risk-off", or
any equivalent trading term unless separately established later under entirely separate governance.
Any admissible object of this kind remains a **research market-state object only**.

`A bounded non-directional volatility-regime filter is a research market-state object, not a trade-gating or execution object.`

## 11. Filter-admissibility criteria applied

A future bounded non-directional filter preregistration would be admissible only if **all** of the
following held on committed evidence:

1. **Non-directionality.** The input object and the output label carry no sign, and no directional
   quantity can be recovered from them.
2. **Object integrity.** The proposed object is a market-state / volatility-magnitude object, not a
   hidden directional signal and not a trading-action object under a research name.
3. **Evidential support.** The underlying pass is block-consistent and uncertainty-supported under
   the preregistered contract, and is correctly classified as development-level rather than
   reserve-confirmed.
4. **Materially different question.** A future filter must answer a question materially different
   from the Phase 4bn-BB forecasting question, and must not be a repackaging of the already-known
   result.
5. **Decision consequence.** Pass or fail of the future filter must materially change the project
   state under existing governance.
6. **Bounded researcher freedom.** The exact mapping from the CF-1 forecast to any state/filter must
   be freezable before any new evidence is opened, with one mapping, one comparator, one consequence
   rule, no menu, no threshold search, no regime-count search, and no post-hoc subgroup path.
7. **Falsifiability without strategy outcomes.** The object must be falsifiable without any
   strategy, PnL, or execution outcome.
8. **Anti-rescue compliance.** It must not reopen, soften, or substitute for any stopped arc, and it
   must not be a disguised rescue of a prior strategy or directional family.
9. **Governance compatibility.** It must remain compatible with the twelve binding M0 clauses where
   applicable, with Phase 4bn-AE §19, and with every preserved lock and flag.

Criteria 1, 2, 3, 6, 7, 8, and 9 are satisfiable. **Criteria 4 and 5 are not satisfied**, and that is
the basis of the decision in §16.

## 12. Scientific-object assessment

**Is the Phase 4bn-BB forecast genuinely non-directional?** **Yes.** The target is realized variance
— a sum of squared one-minute log returns — modelled in log space; it carries no sign by
construction. The two retained features (`rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`)
are sign-invariant count and unsigned-volume accumulators; every aggressor-signed, imbalance, and
signed-return column was excluded at Phase 4bn-AY §19. Neither the forecast nor any monotone
transformation of it can produce a direction.

**Would the proposed downstream object still be a volatility-magnitude / market-state object?** As
defined in §10, **yes** — a state label derived from a magnitude forecast contains no sign either.
The risk is not that the object is secretly directional; it is that the object's only natural
consumers are prohibited (§13, §14).

**Is the pass block-consistent and uncertainty-supported under the preregistered contract?** **Yes.**
`D_i > 0` in 7/7 blocks against a preregistered `≥ 6/7` requirement, and `LB_95 =
0.006273843055395148 > 0` under the frozen stratified moving-block bootstrap (10,000 replicates,
`PCG64`, seed `20260715`). P2 and P3 were preregistered as independent and neither substituted for
the other.

**Is the evidence development-level rather than reserve-confirmed?** **Development-level.** The run
used only the 244-date primary execution-access window (2024-03-01 .. 2024-10-31 excluding
2024-10-01). `PRE_V002_INTERNAL_HOLDOUT` is `CONSUMED` and was not used; `V002_TERMINAL_WINDOW` and
`V002_SEALED_TEST` remain `UNTOUCHED_RESERVED`; `test_rows_loaded = 0`. Phase 4bn-AY §20 and §31 both
state that a development-level pass is not reserve-confirmed evidence.

## 13. Decision-consequence test

This is the decisive section. Each question is answered on committed evidence.

**(a) Would a future bounded filter answer a question materially different from the Phase 4bn-BB
forecasting question?**

**Not materially.** A state/regime label built from the frozen CF-1 forecast is a **coarsening** of
that forecast. Phase 4bn-BB already compared the augmented forecast against the nested HAR baseline
under a proper variance score, block by block, with uncertainty. Discretizing the same forecast into
state labels and comparing the same two nested models under a state-level criterion asks a strictly
weaker version of the same question: the state object carries no information the continuous forecast
does not already carry, and it discards information in the process.

There is one genuinely non-derivable quantity — the **rate at which baseline-derived and
augmented-derived state labels disagree** — which is not determined by `ρ = 0.036651473671709504`,
since two forecasts can be close in aggregate loss and still disagree frequently near a boundary, or
far apart in loss and rarely disagree. That is the strongest available candidate for a materially
different question, and it is addressed in §15.

**(b) Would pass or fail of a future filter materially change the project state?**

**No, asymmetrically and adversely.**

- A **pass** would authorize nothing. Every consumer of a market-state label — entry/exit gating,
  sizing, timing, risk budgeting, portfolio allocation, cost optimization, live risk control — is
  prohibited absolutely by the Phase 4bn-AE §19 boundary and by the unmet twelve-clause M0 gate for
  any strategy path. A pass would therefore leave the project in exactly its present posture, while
  supplying the strongest available "a market-state filter works" framing — precisely the
  momentum-by-success pressure that Phase 4bn-AX §17 identified as a bounded condition of the CF-1
  selection.
- A **fail** would be confounded. A negative state-level result is attributable either to the
  substrate carrying no decision-relevant magnitude information **or** to information loss from
  discretization. The design cannot separate those, so a fail would not cleanly close anything that
  Phase 4bn-BB has not already bounded.

This is the inverse of the asymmetry that justified CF-1 itself. At Phase 4bn-AX §14/§16 the CF-1
**null** was the high-value outcome: it would have retired the trade-tape substrate on the magnitude
axis, a large open question, at near-zero cost. Here the only potentially useful outcome is a fail,
and that fail is both confounded and small: it would establish that an effect the project has
already declined to call material is also not material after coarsening.

**(c) Is the filter merely repackaging the already-known 3.67% QLIKE result?**

**Substantially yes.** Under the criteria of §10 and §11, and with row-level prediction inspection
prohibited, the admissible design space collapses to: apply one frozen mapping to the two nested
forecasts already compared in Phase 4bn-BB, then compare them again under a coarser criterion.
Phase 4bn-AY §29 already prohibits treating secondary metrics as primary and prohibits subgroup or
regime mining; the honest description of what remains is a re-expression of `Δ_equal` and the seven
`D_i`.

**(d) Is a filter continuation scientifically useful without claiming trading utility?**

**Marginally at best.** Stripped of every prohibited consumer, the residual scientific content is
"how large is the already-measured effect, expressed as a state-label disagreement rate". That is a
descriptive quantity. Phase 4bn-AX §16 and the Phase 4bn-AS §26 cost/benefit gate both weigh
expected decision-relevant information gain, not descriptive interest. The expected decision-relevant
gain here is low.

**Three of the four decision-consequence tests are not cleanly answered in favour of continuation.**
Per the governing standard that a failure to answer these cleanly weighs against continuation, this
is decisive.

## 14. Researcher-freedom assessment

**Can a future filter be preregistered with one state mapping and one consequence rule before
evidence access?** **Yes, in principle.** Phase 4bn-BA is the governing precedent: it selected the
corrected feature pair from **source definitions only**, with no data opened and no result in
existence, and recorded the selection as demonstrably not data-driven (BA audit §12, §16).

**Can threshold and regime freedom be bounded without mining the Phase 4bn-BB predictions?**
**Structurally, yes — and this is the strongest single point in favour of continuation.** The
committed Phase 4bn-BB record contains per-block QLIKE, the seven `D_i`, `Δ_equal`, `ρ`, `LB_95`,
secondary MSE and Mincer–Zarnowitz R², condition numbers, ranks, and counts. It contains **no
forecast distribution, no quantile, no per-origin prediction, and no state-relevant scale
information**. A mapping expressed in train-only quantile terms of the frozen forecast therefore
cannot be reverse-engineered from anything on `main`, and the local artefact roots are barred from
inspection. The anti-post-hoc position is genuinely defensible.

**But researcher freedom is not thereby eliminated, only relocated.** Committed governance forces
neither the number of states, nor the mapping family, nor the state-level criterion, nor the
comparator. Unlike CF-1 itself — whose baseline (HAR-RV), loss (QLIKE), horizon, and cadence were
each anchored in canonical external theory or committed support at Phase 4bn-AY §14–§22 — no
external canonical form forces a state object here. Any such choice would be a convention selected by
the author, and it would be selected by an author who has necessarily read the Phase 4bn-BB result.
That is a materially weaker anti-post-hoc position than Phase 4bn-BA enjoyed, where no result existed
at all.

**Can neighbouring variants be prohibited clearly?** **Yes** — Phase 4bn-AY §29/§30 and M0.10 supply
the language.

**Can the filter be falsified without strategy or PnL outcomes?** **Yes** — a state-level proper
score or a disagreement-rate predicate is computable with no execution, no cost model, and no PnL.

**Net.** Researcher freedom is boundable but not forced; the object is anchorable but not canonical.
This is not by itself disqualifying, and it is not the basis of the decision. It compounds §13.

## 15. Anti-post-hoc analysis

A future preregistration would have to be prohibited from selecting, on the basis of the observed
Phase 4bn-BB result:

| Prohibited post-hoc selection | Reachable from committed evidence? | Status |
|---|---|---|
| A threshold chosen to maximize Phase 4bn-BB QLIKE improvement | No — no forecast-scale value is committed | Prohibited |
| A threshold chosen from the block-specific `D_i` | The seven `D_i` are committed; they carry no forecast-scale information | Prohibited |
| A threshold chosen from the bootstrap distribution | Only `LB_95` is committed, not the replicate distribution | Prohibited |
| A threshold chosen from secondary MSE or Mincer–Zarnowitz R² | Both aggregates are committed; neither carries forecast-scale information | Prohibited |
| A regime boundary chosen after examining predictions | Row-level prediction inspection is prohibited; the artefact root is barred | Prohibited |
| A regime count selected after examining outcomes | Not reachable; also independently prohibited | Prohibited |
| A forecast transformation selected after examining outcomes | Not reachable; also independently prohibited | Prohibited |
| A subgroup, month, or block selected because Phase 4bn-BB performed best there | B2 and B7 are visibly the largest `D_i` on `main`; **this is reachable** | Prohibited; the reachability is a real hazard |
| A direction or strategy rule inferred from magnitude behaviour | Not inferable; direction is absent by construction | Prohibited |

The one genuinely reachable hazard is subgroup/block selection: the committed per-block table makes
B2 (`+2.152699e-02`) and B7 (`+1.867419e-02`) visibly the strongest and B4 (`+2.492981e-03`) and B1
(`+2.801856e-03`) visibly the weakest. Any future design that weighted, ordered, sequenced, or
restricted evaluation blocks would be contaminated. Phase 4bn-AY §29 already forbids post-hoc
exclusion of adverse dates or blocks and block-boundary adjustment after results, so the prohibition
exists; but the information is now public within the repository, which is a permanent one-way change
relative to the pre-Phase 4bn-BB position.

**Phase 4bn-BC itself selects nothing.** This phase chooses no numeric filter threshold, no regime
boundary, no regime count, no mapping, no comparator, no state criterion, and no consequence rule. No
choice of regime count is forced by binding prior governance, and none is made here. No row-level
prediction was inspected.

`No numeric filter threshold, regime boundary, regime count, strategy rule, or trading action is selected by Phase 4bn-BC.`

## 16. Decision A — options and selected decision

**Option A — `SELECT_BOUNDED_NON_DIRECTIONAL_CF1_FILTER_FOR_SEPARATE_PREREGISTRATION`.** Not
selected. The scientific-object tests (§12), researcher-freedom tests (§14), anti-post-hoc tests
(§15), stopped-family tests (§18), and governance tests (§19) are individually survivable; the
decision-consequence tests (§13) are not. A continuation whose pass authorizes nothing, whose fail is
confounded with discretization loss, and whose residual content is a re-expression of an
already-committed aggregate does not meet the admissibility criteria in §11(4) and §11(5).

**Option B — `DEFER_CF1_FILTER_PREREGISTRATION__CONSEQUENCE_NOT_YET_SUFFICIENTLY_BOUNDED`.** Not
selected. Deferral requires a genuine unresolved **governance or design gap** that a separate
docs-only resolution phase could close. The blocker identified here is not procedural. No governance
document can manufacture decision consequence for an object whose every consumer is prohibited by
Phase 4bn-AE §19 and by the unmet M0 gate, and no standard can un-coarsen a coarsening. Writing a
state-object standard would produce paperwork without changing the answer. Deferral would also leave
the momentum-by-success pressure of Phase 4bn-AX §17 open indefinitely rather than resolving it.

**Option C — `REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED`. Selected.**

### Exact Decision A

```
REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED
```

### Reason for the selected decision

The Phase 4bn-BB valid pass is real, correctly obtained under a contract frozen before any data was
opened, block-consistent at 7/7, uncertainty-supported at `LB_95 = 0.006273843055395148`, and
numerically sound at augmented condition numbers of roughly `3.983e2`–`6.494e2` against a `> 1e10`
guard. It is preserved in full and is not narrowed, softened, downgraded, or reinterpreted by this
decision. What it supports is exactly what Phase 4bn-AX §14 and Phase 4bn-AY §31 said it would:
development-level incremental one-hour realized-volatility magnitude information, and a docs-only
assessment of whether a bounded non-directional filter could follow.

That assessment answers **no**, on the predeclared decision-consequence test rather than on any new
scientific ground. A bounded non-directional market-state object built from the frozen CF-1 forecast
is a coarsening of a comparison the project has already completed. Its pass would authorize nothing,
because every consumer of a market-state label is barred absolutely; its fail would be confounded
between "no decision-relevant information" and "information lost to discretization". The residual
non-derivable content — a state-label disagreement rate — is descriptive, and the expected
decision-relevant information gain does not justify another evidence-opening arc under the same
cost/benefit reasoning that Phase 4bn-AS §26 applied when it stopped the long-horizon ML arc and that
Phase 4bn-AT §54 applied when it stopped the top-of-book arc.

The project does not gain by converting every statistically informative forecast into downstream
work. It gains by recording what the substrate does and does not support and stopping there. The
substrate is now characterized on both axes it can be characterized on with admissible data:
directionally thin and horizon-degrading (Phase 4bn-AJ / AR / AS), and incrementally informative on
magnitude at a development level (Phase 4bn-BB). That is a complete, honest, and durable scientific
record. Continuation would add a coarser restatement of the second half of it, at the cost of new
researcher freedom, a permanently weaker anti-post-hoc position, and the strongest trading-adjacent
framing the project has yet had available.

## 17. Strongest counterarguments and responses

### 17.1 Strongest case against continuing CF-1 into a filter (adopted)

Stated as required, and adopted as the basis of the decision:

- **A volatility forecast may be scientifically informative but decision-inert.** This was Fable's
  strongest self-objection at Phase 4bn-AX §10 and the core of the select-none case at Phase 4bn-AX
  §27. It was answered there by CF-1's high negative-result value. That answer does not carry over:
  the filter has no comparable null.
- **A 3.67% relative QLIKE improvement need not translate into a meaningful market-state
  distinction.** The project has never adopted any magnitude threshold for materiality; Fable's
  illustrative 3–5% margin was explicitly not adopted and is not repository policy (Phase 4bn-AX §10;
  Phase 4bn-AY §22). There is therefore no committed standard by which the observed `ρ` could be
  called large enough to matter — and inventing one now would be selection from the observed result.
- **Converting a successful forecast into a filter introduces arbitrary threshold and regime
  freedom.** Confirmed at §14: no committed governance and no canonical external theory forces the
  regime count, mapping family, state criterion, or comparator.
- **Using a filter to gate trades would become strategy logic and is prohibited.** Phase 4bn-AE §19
  is absolute; M0.5 cost realism, execution feasibility, and slippage/spread cannot be supported by
  aggTrades-only data at all.
- **The project may gain more by preserving evidence and stopping after establishing substrate
  informativeness.** Both reserves remain untouched and `test_rows_loaded = 0`; stopping here costs
  nothing and preserves everything.

### 17.2 Strongest case against the selected decision, and why it does not prevail

The strongest case for Option A is not weak and is stated here in full.

Phase 4bn-AX §14 predeclared, before any data existed, that a pass would permit a bounded
non-directional filter assessment — and a phase that answers "no" to its own predeclared continuation
can look like a project that moves the goalposts after obtaining a positive result. Worse, the
anti-post-hoc position is objectively defensible: the committed record contains no forecast-scale
information, so a train-only quantile mapping frozen ex ante genuinely could not be reverse-engineered
from anything on `main`. Every item on the Option-A structural checklist (§20) is `NO`. And there is
one genuinely non-derivable quantity — the baseline-versus-augmented state-label disagreement rate —
which is **not** determined by `ρ`, so the "pure repackaging" charge is not strictly true. On that
reading, a bounded state-disagreement study is a small, clean, cheap, non-directional question whose
null would definitively retire the decision-relevance of the CF-1 effect, exactly as CF-1's own null
would have retired the magnitude axis.

**Why it does not prevail.** The decisive criterion is decision consequence, and it fails on the
asymmetry rather than on the novelty. Even granting that the disagreement rate is a genuinely new
quantity, only one of its two outcomes is useful. A high-disagreement result authorizes nothing —
every consumer is barred by Phase 4bn-AE §19 and by an M0 gate that aggTrades-only evidence cannot
clear — while supplying maximal momentum pressure of exactly the kind Phase 4bn-AX §17 bounded as a
condition of selection. A low-disagreement result closes a lane the committed record already bounds:
Phase 4bn-BB itself states that no economic materiality, transaction-cost clearance, or tradability
is established, so "the effect is also small at state granularity" is a marginal addition. An
experiment with one uninformative outcome and one marginal outcome does not clear the cost/benefit
gate that Phase 4bn-AS §26 applied to a scarce-reserve confirmation and that Phase 4bn-AT §49/§54
applied to an acquisition — and both of those precedents stopped on materially stronger prospective
gains than this.

Nor does the predeclaration bind toward continuation. Phase 4bn-AX §14 permits "a separate later
docs-only assessment of **whether** the forecast **could** support" such a filter. That is a question,
and answering it negatively on the predeclared decision-consequence criterion is faithful execution.
Phase 4bn-AX §28 itself made decision consequence the decisive criterion when it selected CF-1; the
same criterion, applied honestly to the successor object, selects against it.

Finally, the anti-post-hoc defensibility cuts both ways. It shows a filter **could** be preregistered
cleanly; it does not show one **should** be. The per-block `D_i` table is now permanently visible on
`main`, which makes subgroup and block-ordering contamination reachable in a way it was not before
(§15). Accepting a permanent increase in contamination surface to buy a study with one uninformative
outcome is not a favourable trade.

The decision therefore stands, and it stands on the same criterion — decision consequence — that
selected CF-1 in the first place. That symmetry is what makes it credible rather than opportunistic.

## 18. Stopped-family, anti-rescue, and cooldown consequence

- **`STOP_LONGHORIZON_ML_ARC`** — not reopened, not softened, not merged, not reinterpreted, not
  rescued. The rejected continuation used no long-horizon label family, no directional target, and no
  classifier. Rejecting it cannot reopen the arc.
- **`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`** — not revived. No top-of-book, bookTicker,
  order-book, quote, depth, or midpoint object was proposed, used, or substituted.
  `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE` is preserved.
- **`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`** — preserved. No proxy is substituted for
  an inadmissible source; no liquidation, forced-flow, or aggressor-imbalance object is introduced.
- **Disguised rescue.** The rejected continuation was assessed for, and this decision closes, the
  possibility that a "market-state filter" becomes a directional or strategy family under a research
  name. No prior strategy family (R2 / F1 / D1-A / V2 / G1 / C1) is revived.
- **Cooled-down families.** M0 §7.A (price-only single-symbol directional continuation) is untouched
  — the object was non-directional. M0 §7.D (microstructure / order-flow / liquidity-timing,
  `NOT_RECOMMENDED_NOW`) is the relevant lane; its relationship is bounded explicitly in the companion
  audit §7. Nothing here relaxes §7.D, and no §6 "materially new mechanism source" is asserted.
- **Anti-rescue on the rejection itself.** Per Phase 4bn-AY §30, this rejection does **not** authorize
  neighbouring variants. No alternative filter family, feature set, horizon, loss, model, or state
  object is proposed as a substitute. The CF-1 filter continuation is closed, not redirected.

## 19. M0 implication summary

The full clause-by-clause mapping is in the companion audit. In summary:

- **Strategy M0 is not cleared and this phase does not clear it.** The Phase 4bn-BB valid pass does
  not clear strategy M0, and neither Phase 4bn-BC nor any future filter object may be described as
  clearing it.
- For any strategy or PnL path the **Phase 4bn-AE §19 boundary remains absolute**, because
  aggTrades-only evidence cannot establish executable spread, slippage, executable mid, depth,
  impact, or execution feasibility. That boundary is untouched and unsoftened.
- Phase 4bn-BC was entitled to determine whether a **non-strategy research filter** is admissible to
  preregister, and determined that it is not, on decision-consequence grounds.
- `research_eligible = false` — unchanged. `eligibility_gate_status = pending` — unchanged. All
  authorization flags remain `false`. The Phase 4aw always-raising `flip_research_eligible(...)`
  behaviour is preserved and was not invoked.

## 20. Structural confirmation checklist

Confirmed for the continuation that was assessed and rejected, and confirmed for this phase's own
conduct:

| Item | Answer |
|---|---|
| Changes the Phase 4bn-BB target | NO |
| Changes the Phase 4bn-BB features | NO |
| Changes the Phase 4bn-BB model | NO |
| Changes the Phase 4bn-BB loss | NO |
| Changes the Phase 4bn-BB horizon | NO |
| Selects a subgroup | NO |
| Selects a month or block | NO |
| Reruns Phase 4bn-BB | NO |
| Adds direction | NO |
| Adds top-of-book or order-book data | NO |
| Adds a liquidation proxy | NO |
| Reopens stopped long-horizon ML | NO |
| Uses reserve data | NO |
| Uses a neighbouring feature set | NO |
| Transforms the Phase 4bn-BB valid pass into a trading claim | NO |

Every item is `NO`. The checklist is therefore **not** the reason Option A was declined; §13 is. The
checklist is recorded to make explicit that the rejection rests on decision consequence and not on
any structural violation, and that Phase 4bn-BC itself commits none of these acts.

## 21. Exact claim-scope table

| Claim | Status after Phase 4bn-BB |
|---|---|
| aggTrades substrate carries incremental one-hour volatility-magnitude information | `SUPPORTED_DEVELOPMENT_LEVEL` |
| corrected CF-1 forecast improves HAR QLIKE under the frozen development contract | `SUPPORTED_DEVELOPMENT_LEVEL` |
| effect is block-consistent | `SUPPORTED_DEVELOPMENT_LEVEL` |
| effect is uncertainty-supported under the frozen bootstrap | `SUPPORTED_DEVELOPMENT_LEVEL` |
| corrected two-feature design is numerically identifiable under the frozen guards | `SUPPORTED_DEVELOPMENT_LEVEL` |
| forecast is directional | `NOT_SUPPORTED` |
| forecast is a trading signal | `NOT_SUPPORTED` |
| forecast is economically material | `NOT_ESTABLISHED` |
| forecast clears 16 bps round trip | `NOT_ESTABLISHED` |
| forecast is profitable | `NOT_SUPPORTED` |
| forecast is tradable | `NOT_SUPPORTED` |
| a forecast-derived market-state object carries decision consequence | `NOT_ESTABLISHED` |
| a bounded non-directional filter continuation is justified | `NOT_SUPPORTED` (Phase 4bn-BC decision) |
| strategy M0 cleared | `NOT_CLEARED` |
| execution feasibility, spread, slippage, depth, or impact established | `NOT_ESTABLISHED` |
| terminal reserve confirmed | `NOT_TESTED_RESERVED` |
| sealed test confirmed | `NOT_TESTED_RESERVED` |
| Phase 4bn-BB may be rerun | `PROHIBITED_CONSUMED` |
| Phase 4bn-AZ may be rerun or reclassified | `PROHIBITED_CONSUMED` |
| consumed pre-v002 internal holdout usable as independent confirmation | `PROHIBITED_CONSUMED` |
| long-horizon ML arc reopened | `PROHIBITED` |
| ToB mechanism arc reopened | `PROHIBITED` |
| forced-flow / liquidation-proxy family reopened | `PROHIBITED` |
| Phase 4bn-AY three-feature set executable | `PROHIBITED` |
| `rolling_quantity_mean_60s` admissible as a CF-1 model feature | `PROHIBITED` |
| `research_eligible` may be flipped | `PROHIBITED` |

No unsupported claim is softened.

## 22. Exact scientific consequence

`The BB valid pass supports development-level incremental one-hour realized-volatility magnitude information only.`

`The BB valid pass does not establish direction, profitability, transaction-cost clearance, tradability, or strategy M0 clearance.`

The Phase 4bn-BC decision adds exactly one consequence and no scientific claim: the CF-1 lane does
not continue into a bounded non-directional market-state / volatility-regime filter preregistration.
The Phase 4bn-BB result stands in full and is not narrowed, downgraded, or reinterpreted. No new
scientific metric is computed, asserted, or implied by this phase, and no row-level inference is made.

## 23. Decision B — reserve posture

### Exact Decision B

```
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

### Rationale

The CF-1 lane should not consume protected evidence. With the filter continuation closed there is no
downstream question in this lane for a terminal-window confirmation to serve, and confirming a
development-level magnitude result that authorizes nothing would be a poor allocation of a scarce,
irreplaceable, one-shot asset — the same reasoning by which Phase 4bn-AS §25 refused to spend a
scarce reserve to confirm a non-actionable finding.

R1 (`NO_RESERVE_PROPOSAL_JUSTIFIED_AT_THIS_STAGE`) would understate the position: R1 describes a lane
whose correct next step remains docs-only or development-only, and under Option C there is no next
step in this lane at all. R2 (`FUTURE_TERMINAL_RESERVE_PROPOSAL_MAY_BE_JUSTIFIED`) is not available:
a future terminal-reserve question would be proportionate only if a decision downstream of it could
change, and every downstream decision remains barred by Phase 4bn-AE §19 and the unmet M0 gate.
Several automatic refusal conditions of the scarce-reserve standard §11 would also be engaged —
unclear decision consequence, no valuable negative result, and missing cost/engineering
proportionality.

R3 is therefore the accurate posture: the CF-1/filter lane does not consume protected evidence, and
the reserves remain reserved.

### Reserve-governance mapping

Regardless of R1 / R2 / R3, and confirmed here: no reserve is opened; the evidence ledger is not
changed; no terminal use is authorized; no sealed-test use is authorized.

```
PRE_V002_INTERNAL_HOLDOUT = CONSUMED
V002_TERMINAL_WINDOW      = UNTOUCHED_RESERVED
V002_SEALED_TEST          = UNTOUCHED_RESERVED
test_rows_loaded          = 0
```

`PRE_V002_INTERNAL_HOLDOUT remains CONSUMED.` It cannot become independent evidence again;
`CONSUMED` is terminal under the evidence-budget ledger §2 and §3.3.

`V002_TERMINAL_WINDOW remains UNTOUCHED_RESERVED.`

`V002_SEALED_TEST remains UNTOUCHED_RESERVED.`

`No evidence reserve is opened or spent by Phase 4bn-BC.`

A development-level Phase 4bn-BB pass is **not** reserve-confirmed evidence. Because R3 is selected,
no reserve-spend proposal is created, drafted, or recommended by this phase; the pre-spend quorum of
the scarce-reserve standard §7/§8/§12 is not engaged, and its requirements remain owned by that
standard unchanged. The sealed test remains the project's highest-protection, single-use reserve; a
terminal-window result would not automatically authorize it, and it would require its own separately
justified proposal in a separate phase under standard §10.C.

## 24. Exact non-authorization state

`No direction, signal, strategy, position sizing, entry/exit logic, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BC.`

Additionally not authorized by this phase: any filter design, filter implementation, or filter
execution; any preregistration; any successor phase; any data read; any model fit; any metric
recomputation; any rerun of Phase 4bn-BB or Phase 4bn-AZ; any data acquisition; any reserve spend;
any manifest, ledger, eligibility, or lock mutation; any merge; any merge-closeout; any network, API,
credential, WebSocket, MCP, Graphify, or `.mcp.json` use.

## 25. Successor envelope

**Not applicable.** Option C is selected, so no successor envelope is defined and no successor is
proposed. `Phase 4bn-BD — CF-1 Bounded Non-Directional Volatility-Regime Filter Preregistration` is
**not** proposed and **not** authorized by this phase; it exists in the record only as the title of
the continuation that Phase 4bn-BC declines. No admissible filter envelope, mapping, threshold,
regime count, comparator, or consequence rule is defined here.

Per Phase 4bn-AY §30, this rejection does not authorize neighbouring variants. Any materially
different future CF-1-adjacent object would require a new mechanism justification, a new docs-only
phase, an explicit anti-duplication audit, and separate operator authorization — and would have to
clear M0 on its own terms.

## 26. Preserved locks and states

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising `flip_research_eligible(...)` behaviour
(never invoked); Phase 4bn-AE §19; the Phase 4ak twelve-clause M0 gate; the Phase 4ak §6 post-null
cooldown rule and the §7 cooled-down-family list; the locked 8 bps/side · 16 bps round trip; the
Phase 4bn-BB no-rerun boundary; every prior verdict; every dataset identity and hash; all split,
holdout, sidecar, and storage policies; the evidence-ledger statuses; and the spending-authority
rules. **No stopped arc is softened, merged, reinterpreted, reopened, or rescued.**

`docs/00-meta/current-project-state.md` is left unchanged by this phase, matching the docs-only
precedent from Phase 4bn-AH through Phase 4bn-BA.

## 27. Recommended operator action

Review the three Phase 4bn-BC files and the final operator report. Then decide separately whether to
authorize a merge phase for Phase 4bn-BC. No merge is performed or authorized here and no
merge-closeout is created.

Recommended posture: **remain paused.** With the CF-1 filter continuation closed and R3 recorded,
there is no recommended successor phase in this lane. Any future research would require a genuinely
new family with its own M0-style admissibility memo and its own separate operator authorization.

`Remaining paused is a valid operator choice.`

## 28. Exact final Phase 4bn-BC result state

```
CF1_VALID_PASS_PRESERVED__FILTER_CONTINUATION_REJECTED__NO_SUCCESSOR_AUTHORIZED__RESERVES_UNTOUCHED__REMAIN_PAUSED
```

Reserve posture (separate field):

```
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

## 29. Exact statements

`Phase 4bn-BB remains CF1_VALID_PASS and its single evidence-bearing run remains consumed.`

`The BB valid pass supports development-level incremental one-hour realized-volatility magnitude information only.`

`The BB valid pass does not establish direction, profitability, transaction-cost clearance, tradability, or strategy M0 clearance.`

`A bounded non-directional volatility-regime filter is a research market-state object, not a trade-gating or execution object.`

`No numeric filter threshold, regime boundary, regime count, strategy rule, or trading action is selected by Phase 4bn-BC.`

`PRE_V002_INTERNAL_HOLDOUT remains CONSUMED.`

`V002_TERMINAL_WINDOW remains UNTOUCHED_RESERVED.`

`V002_SEALED_TEST remains UNTOUCHED_RESERVED.`

`No evidence reserve is opened or spent by Phase 4bn-BC.`

`No direction, signal, strategy, position sizing, entry/exit logic, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BC.`

`Remaining paused is a valid operator choice.`
