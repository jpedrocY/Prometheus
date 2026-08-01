# Phase 4bn-BC — Closeout

## 1. Phase identity

**Phase 4bn-BC — CF-1 Valid-Pass Filter-Admissibility and Consequence Assessment.** A docs-only
decision and governance assessment phase that made exactly one primary decision about the consequence
of the merged Phase 4bn-BB `CF1_VALID_PASS`, plus one separate evidence-governance decision.

## 2. Branch and base

- **Branch:** `phase-4bn-bc/cf1-valid-pass-filter-admissibility-consequence-assessment`.
- **Base `main` == `origin/main` == `HEAD` at branch creation:**
  `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49` (Phase 4bn-BB merge-closeout SHA-finalization tip),
  unchanged throughout.
- Required lineage confirmed before any mutation: Phase 4bn-BB no-fast-forward merge
  `0200d576884ae8461f75768b97b8ad9d938a8a9b`; Phase 4bn-BB merge-closeout branch commit
  `4214c658fea625be1d626af99324c5c0babea57c`; Phase 4bn-BB pre-merge closeout
  `345165710ddb17622d6c679e2d350f2779022068`; Phase 4bn-BB result
  `6ba76b56a514cb0abaeac0480a59a688a7cdebeb`; Phase 4bn-BB implementation
  `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917`; Phase 4bn-BA finalization / Phase 4bn-BB base
  `e26193e8f61cae797e4cbfab932025b709b74566`.

## 3. Phase type and risk tier

- **Phase type:** docs-only; decision and governance assessment only. No data; no model; no metric
  recomputation; no filter implementation; no filter execution; no reserve-spend authorization; no
  strategy / PnL / backtest authorization.
- **Risk tier:** Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it
  decides the downstream consequence of the project's only positive scientific result, so it takes the
  highest ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, ledger, or
  lock.

## 4. Files added (exactly three)

- `docs/00-meta/implementation-reports/2026-07-31_phase-4bn-bc_cf1-valid-pass-filter-admissibility-and-consequence-assessment.md`
- `docs/00-meta/implementation-reports/2026-07-31_phase-4bn-bc_cf1-m0-evidence-budget-and-anti-rescue-audit.md`
- `docs/00-meta/implementation-reports/2026-07-31_phase-4bn-bc_closeout.md` (this file)

Relative to base `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49`, the branch contains exactly three `A`
entries and no `M`, `D`, or `R`.

## 5. No existing file modified

**No existing file was modified, deleted, or renamed.** No source, test, script, config, manifest,
ledger, process standard, phase gate, or technical-debt entry was created or changed. No reserve
proposal and no successor prompt was created. `docs/00-meta/current-project-state.md` and `README` are
left unchanged, matching the docs-only precedent from Phase 4bn-AH through Phase 4bn-BA. No
`data/microstructure/` or `data/research/` path was staged or committed.

## 6. Documents inspected

Phase 4bn-BB: the corrected-execution-and-verdict report, the artefact/leakage/split-validation
report, the closeout, and the merge-closeout. Phase 4bn-BA: the feature-contract correction and
re-preregistration, the estimability and anti-duplication audit, and the corrected-execution
validation checklist. CF-1 selection / consequence lineage: Phase 4bn-AX candidate-selection and
decision-consequence memo with its forced-flow overlap / proxy-validity / M0 audit; Phase 4bn-AY
substrate-test preregistration and implementation-grade target/feature/baseline/evaluation contract.
Stopped-arc lineage: Phase 4bn-AK, Phase 4bn-AS, Phase 4bn-AT. Binding governance:
`docs/00-meta/m0-mechanism-admissibility-gate.md`; Phase 4bn-AE preregistration-contract amendment
(especially §19); `docs/00-meta/process/evidence-budget-ledger.md`;
`docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md`; Phase 4bn-AV;
Phase 4bn-Y split / holdout policy as restated in the ledger and Phase 4bn-AY §20/§21;
`docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`. Process standards
under `docs/00-meta/process/`: phase-workflow, phase-risk-tiering, operator-report, merge-closeout,
phase-prompt-template, context-management, and lightweight-workspace. Git metadata for base-state
verification.

## 7. No data / execution / network statement

Nothing under `data/microstructure/` or `data/research/` was opened, read, listed for content,
sampled, parsed, hashed, or scored. The Phase 4bn-BB v002 and Phase 4bn-AZ v001 local artefact roots
were not inspected. No Parquet, local research JSON, or sidecar was opened. No QLIKE value, bootstrap
replicate, or condition number was recomputed. No model was fitted; no target or feature was
generated. The Phase 4bn-BB runner was not invoked in `--preflight` or `--run` form. No project
script, builder, diagnostic, backtest, replay, or runtime process was run. `pytest`, Ruff, and mypy
were not run. No network, web, API, or Binance endpoint was used; no credential, `.env`, WebSocket,
MCP, Graphify, or `.mcp.json` was used; no external reviewer was used. No row-level prediction was
inspected. Every scientific value in the Phase 4bn-BC documents is transcribed verbatim from the
committed Phase 4bn-BB reports.

## 8. Exact Phase 4bn-BB scientific outcome (preserved)

```
CF1_VALID_PASS
```

Merged result state on `main`, preserved exactly:

```
CF1_CORRECTED_VALID_PASS_MERGED_TO_MAIN__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__NO_RERUN_AUTHORIZED__DOCS_ONLY_FILTER_ASSESSMENT_REQUIRED_BEFORE_ANY_DOWNSTREAM_ACTION__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

Evidence preserved unchanged: corrected pair `rolling_aggtrade_count_60s` and
`rolling_quantity_sum_60s`; prohibited feature `rolling_quantity_mean_60s`; candidate 5,854 / valid
5,516 / invalid 338 (`har_unavailable` 336, `har_coverage_failure` 2), zero-RV 0; all seven `D_i`
positive; equal-weighted QLIKE baseline `0.32573980348957254` and augmented `0.31380095965814664`;
`Δ_equal = 0.011938843831425896`; `ρ = 0.036651473671709504`; bootstrap 10,000 replicates, `PCG64`,
seed `20260715`, `LB_95 = 0.006273843055395148`; `P1 = P2 = P3 = validity = true` with P2 at 7/7;
baseline rank 4/4 and augmented rank 6/6 in all seven blocks; augmented condition numbers
approximately `3.983e2`–`6.494e2` against the frozen `> 1e10` invalidation threshold.

`Phase 4bn-BB remains CF1_VALID_PASS and its single evidence-bearing run remains consumed.`

## 9. Exact Decision A

```
REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED
```

Basis: the decision-consequence test. A bounded non-directional market-state object built from the
frozen CF-1 forecast is a coarsening of a comparison Phase 4bn-BB has already completed; its pass
would authorize nothing because every consumer of a market-state label is barred absolutely by Phase
4bn-AE §19 and by the unmet twelve-clause M0 gate; its fail would be confounded between "no
decision-relevant information" and "information lost to discretization"; and the residual
non-derivable content is descriptive. Structurally the continuation was admissible — every item on
the Option-A checklist is `NO` — but admissibility is necessary and not sufficient. Option B was
declined because the blocker is scientific rather than procedural and no governance document could
close it. The Phase 4bn-BB valid pass is preserved in full and is not narrowed, downgraded, or
reinterpreted.

## 10. Exact Decision B

```
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

Basis: with the filter continuation closed there is no downstream question in this lane for a
terminal-window confirmation to serve, and confirming a development-level magnitude result that
authorizes nothing would be a poor allocation of a scarce, irreplaceable, one-shot asset — the
reasoning Phase 4bn-AS §25 applied. Several automatic refusal conditions of the scarce-reserve
standard §11 would be engaged (unclear decision consequence; no valuable negative result; missing
cost/engineering proportionality). No reserve proposal is created and the pre-spend quorum is not
engaged.

## 11. Exact final result state

```
CF1_VALID_PASS_PRESERVED__FILTER_CONTINUATION_REJECTED__NO_SUCCESSOR_AUTHORIZED__RESERVES_UNTOUCHED__REMAIN_PAUSED
```

Reserve posture (separate field):

```
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

## 12. Claim-scope consequence

Supported at development level only: that the aggTrades substrate carries incremental one-hour
volatility-magnitude information; that the corrected CF-1 forecast improves HAR QLIKE under the frozen
development contract; that the effect is block-consistent; that it is uncertainty-supported under the
frozen bootstrap; and that the corrected two-feature design is numerically identifiable under the
frozen guards.

Not supported: that the forecast is directional; that it is a trading signal; that it is profitable;
that it is tradable. Not established: economic materiality; clearance of the 16 bps round trip;
decision consequence of a forecast-derived market-state object; execution feasibility, spread,
slippage, depth, or impact. Not cleared: strategy M0. Not tested and reserved: the terminal window and
the sealed test. Prohibited: rerunning Phase 4bn-BB or Phase 4bn-AZ; reusing the consumed pre-v002
internal holdout as independent confirmation; reopening the long-horizon ML arc, the ToB mechanism
arc, or the forced-flow / liquidation-proxy family; executing the Phase 4bn-AY three-feature set;
using `rolling_quantity_mean_60s` as a CF-1 model feature; flipping `research_eligible`.

The full table is in the main memo §21. No unsupported claim is softened.

## 13. M0 and Phase 4bn-AE §19 consequence

**Strategy M0 is not cleared.** The Phase 4bn-BB valid pass does not clear strategy M0, and neither
Phase 4bn-BC nor any future filter object may be described as clearing it. The assessed continuation
was mapped clause by clause in the companion audit:

The assessed continuation is M0-permissible in form. **M0.2 passes because the mechanism source is
non-price-only.** **M0.12 records no post-null reopening** because Phase 4bn-BB returned
`CF1_VALID_PASS` rather than `NOT_SUPPORTED`, so the §6.A materially-new-source requirement is **not
triggered**. M0.3 and M0.7 remain hollow in substance; **M0.8 passes**. Section 7.D remains engaged,
bounded, unrelaxed, and `NOT_RECOMMENDED_NOW`. **M0.5 remains unresolved and blocking for every
trading path.** **Strategy M0 remains NOT CLEARED.**

The substantial forecast-to-state coarsening of Phase 4bn-BB remains adverse under the
anti-duplication and decision-consequence analyses, not as an M0.2 or M0.12 failure; the rejection
continues to rest on decision consequence and anti-duplication.

**Phase 4bn-AE §19 remains absolute and unsoftened.** No result, however strong, authorizes strategy
construction, signal generation, threshold trading, confidence-gated trading, backtesting, PnL
computation, position sizing, execution logic, live-readiness, paper/shadow trading, or
exchange-write. aggTrades-only evidence cannot establish executable spread, slippage, executable mid,
depth, impact, or execution feasibility.

`research_eligible = false`; `eligibility_gate_status = pending`; all authorization flags remain
`false`; the Phase 4aw always-raising `flip_research_eligible(...)` behaviour is preserved and was not
invoked.

## 14. Reserve posture and evidence-ledger state

No reserve was opened or spent. The evidence ledger is unchanged: no row added, edited, or deleted;
no transition-history row appended.

```
PRE_V002_INTERNAL_HOLDOUT = CONSUMED
V002_TERMINAL_WINDOW      = UNTOUCHED_RESERVED
V002_SEALED_TEST          = UNTOUCHED_RESERVED
test_rows_loaded          = 0
```

`PRE_V002_INTERNAL_HOLDOUT remains CONSUMED.` It cannot become independent evidence again.

`V002_TERMINAL_WINDOW remains UNTOUCHED_RESERVED.`

`V002_SEALED_TEST remains UNTOUCHED_RESERVED.`

`No evidence reserve is opened or spent by Phase 4bn-BC.`

A development-level Phase 4bn-BB pass is not reserve-confirmed evidence. A terminal-window result
would not automatically authorize the sealed test; the sealed test remains the highest-protection,
single-use reserve and would require a later, separately justified proposal in a separate phase.

## 15. Preserved locks

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising `flip_research_eligible(...)` behaviour (never
invoked); Phase 4bn-AE §19; the Phase 4ak twelve-clause M0 gate with its §6 cooldown rule and §7
cooled-down-family list; the locked 8 bps/side · 16 bps round trip; the Phase 4bn-BB no-rerun
boundary; every prior verdict; every dataset identity and hash; all split, holdout, sidecar, and
storage policies; the evidence-ledger statuses; and the spending-authority rules. **No stopped arc is
softened, merged, reinterpreted, reopened, or rescued.**

## 16. Working-tree state

Working tree clean except the transient untracked `.claude/scheduled_tasks.lock`, which was never
staged, modified, deleted, cleaned, or committed. No local artefact is tracked and no data is
committed. `main == origin/main == 7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49`, unchanged.

## 17. Merge non-authorization

**No merge is performed or authorized. No merge-closeout is created.** A merge of Phase 4bn-BC, if
desired, requires a separate operator decision and a separate authorized merge phase.

## 18. Successor non-authorization

**No successor phase is authorized and no successor prompt is drafted.** Because Option C was
selected, no successor envelope is defined and no successor is proposed.
`Phase 4bn-BD — CF-1 Bounded Non-Directional Volatility-Regime Filter Preregistration` is **not**
proposed and **not** authorized; it exists in the record only as the title of the continuation this
phase declines. No reserve-spend proposal and no sealed-test proposal is created.

Per Phase 4bn-AY §30, this rejection does not authorize neighbouring variants. Any materially
different future CF-1-adjacent object would require a new mechanism justification, a new docs-only
phase, an explicit anti-duplication audit, separate operator authorization, and its own M0 clearance.

## 19. Commit history and final commit self-reference convention

Phase 4bn-BC has **two commits**. The three files were initially added in one phase commit, followed
by one narrow correction commit modifying two of those three files.

**1 — Initial Phase 4bn-BC decision commit.**

```text
SHA:     bcf3685722187757eaceab2d609a8df01e34b8fa
Message: docs(phase-4bn-bc): assess CF-1 filter admissibility and consequences
```

Role: adds all three Phase 4bn-BC documents; records Decision A, Decision B, and the original
governance audit.

**2 — M0 mapping correction commit.**

```text
Message: docs(phase-4bn-bc): correct M0 clause mapping
```

Role: corrects M0.2 from adverse to **PASS** through the non-price-only source route; corrects M0.12
from adverse to **PASS** because no post-null reopening occurs; preserves the §7.D caution; preserves
Decision A, R3, and the final Phase 4bn-BC result state; and synchronizes this closeout.

**Self-reference convention.** A commit cannot embed its own SHA.

```text
M0 mapping correction commit SHA:
this update (`docs(phase-4bn-bc): correct M0 clause mapping`);
its exact SHA is the resulting final Phase 4bn-BC branch tip and is recorded in
the final operator report and Git log.
```

The correction commit modifies only the companion audit and this closeout; it creates no file and
leaves the main decision memo byte-identical to `bcf3685722187757eaceab2d609a8df01e34b8fa`. Relative
to base `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49` the branch still shows exactly three added Phase
4bn-BC files, with no modification, deletion, or rename of any pre-existing base path.

## 20. Recommended next operator action

Review the three Phase 4bn-BC files and the final operator report. Then decide separately whether to
authorize a merge phase for Phase 4bn-BC. No merge is performed or authorized here.

Recommended posture: **remain paused.** With the CF-1 filter continuation closed and R3 recorded,
there is no recommended successor phase in this lane.

`Remaining paused is a valid operator choice.`

`No direction, signal, strategy, position sizing, entry/exit logic, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BC.`
