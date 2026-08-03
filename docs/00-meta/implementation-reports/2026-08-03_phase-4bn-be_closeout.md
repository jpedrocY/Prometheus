# Phase 4bn-BE — Closeout

## 1. Phase

```text
Phase 4bn-BE — External-Theory New-Lane Discovery and Mechanism-Admissibility Shortlist
```

Docs-only external-theory research and governance screening phase. Tier 1 / Full Phase.

## 2. Branch

```text
phase-4bn-be/external-theory-new-lane-discovery-admissibility-shortlist
```

Created from `main` only after live verification passed. No additional branch was created. No work was
performed on `main`, and `main` was not modified.

## 3. Verified base SHA

```text
fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0
```

Verified live before branch creation, not assumed from the Project-Control snapshot:

```text
git status --short        -> ?? .claude/scheduled_tasks.lock   (only item)
git rev-parse main        -> fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0
git rev-parse origin/main -> fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0
git branch --show-current -> main
git log --oneline -12     -> tip fe28cfc "docs(phase-4bn-bc): finalize merge closeout shas"
```

`main == origin/main == fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0` at branch creation. Phase 4bn-BC is
merge-closeout recorded and project-complete (`4236d19` no-fast-forward merge; `fe28cfc` SHA-finalization
tip). No later committed verdict, lock, reserve state, or authorization shift exists.

The transient untracked `.claude/scheduled_tasks.lock` was present throughout and was never staged,
modified, deleted, cleaned, moved, or committed.

## 4. Files added

Exactly two, both new, both under `docs/00-meta/implementation-reports/`:

```text
A  docs/00-meta/implementation-reports/2026-08-03_phase-4bn-be_external-theory-new-lane-discovery-and-admissibility-shortlist.md
A  docs/00-meta/implementation-reports/2026-08-03_phase-4bn-be_closeout.md
```

## 5. Confirmation that no existing file changed

Confirmed. Base-to-tip diff shape is exactly two `A` entries, zero `M`, zero `D`, zero `R`.

No existing tracked file was modified, deleted, or renamed. Specifically unchanged:
`docs/00-meta/current-project-state.md`; `CLAUDE.md`; `README.md`;
`docs/00-meta/m0-mechanism-admissibility-gate.md`; `docs/00-meta/process/evidence-budget-ledger.md`;
`docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md`;
`docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`.

`D:\Prometheus-Project-Control` was read as context only and **was not modified**. No narrow continuity
write scope existed for this phase and none was used.

## 6. Primary-source research scope

External research was read-only and confined to publicly accessible primary sources: peer-reviewed
journal articles, working papers from recognized academic and institutional repositories (arXiv, NBER,
BIS), official exchange market-structure and contract documentation, and authors' own project sites and
replication documentation. Secondary material was used only to locate primary sources and carries no
substantive claim in the report.

**Thirteen primary sources were retrieved or bibliographically verified** and are tabulated in the main
report §6.1 with authors, title, year, venue, identifier, the mechanism claim each supports, and the
limitation each carries for Prometheus:

Roll (1984, JF, DOI `10.1111/j.1540-6261.1984.tb03897.x`); Corwin & Schultz (2012, JF, DOI
`10.1111/j.1540-6261.2012.01729.x`); Abdi & Ranaldo (2017, RFS, DOI `10.1093/rfs/hhx084`); Ardia, Guidotti
& Kroencke (2024, JFE 161:103916, DOI `10.1016/j.jfineco.2024.103916`); Goyenko, Holden & Trzcinka (2009,
JFE 92:153–181); He, Manela, Ross & von Wachter (2024, `arXiv:2212.06888`); Ackerer, Hugonnier & Jermann
(2024/2026, `arXiv:2310.11771`, NBER WP 32936, DOI `10.1111/mafi.70018`); Schmeling, Schrimpf & Todorov
(BIS Working Papers No 1087); Binance official funding-rate documentation (accessed 2026-08-03); Lillo &
Farmer (2004, SNDE 8(3)); Andersen & Bondarenko (2014, JFM 17(1):1–46); Clark (1973, Econometrica, DOI
`10.2307/1913889`); Ané & Geman (2000, JF, DOI `10.1111/0022-1082.00286`).

A further set of works is **named without bibliographic verification** in the negative-search log
(main report §6.2). None carries a substantive claim, and no rejection rests on any of them.

**Retrieval limitations are recorded explicitly** in main report §6.3 and were counted *against*
candidates rather than resolved by any prohibited means: publisher access failures (HTTP 403 / 402), an
inability to render research PDFs to text in this environment, and the fact that the authoritative route
to the BTCUSDT tick size is a forbidden endpoint call.

## 7. External network activity performed

Permitted and performed: bibliographic web searches; read-only retrieval of publisher, academic
repository, institutional, author-project-site, package-registry, and official exchange documentation web
pages; DOI and citation verification. Four ordinary research PDFs were fetched by the retrieval tool into
a temporary session tool-results directory outside the repository; none was committed, none resides under
`D:\Prometheus`, and none could be rendered to text.

Not performed: any Binance API or exchange endpoint call; any market-data download; any historical trade,
quote, order-book, liquidation, funding, open-interest, or derivatives-data acquisition; any authenticated
service; any credential or `.env` use; any WebSocket; any MCP or Graphify use; any package installation;
any external repository clone; any execution of external code; any executable download.

**No external datum was used to calculate any Prometheus result.**

## 8. Confirmation that no market data or reserve was accessed

Confirmed. No market data of any kind was opened, read, downloaded, sampled, parsed, hashed, or scored.

```text
PRE_V002_INTERNAL_HOLDOUT  = CONSUMED               (unchanged; terminal)
V002_TERMINAL_WINDOW       = UNTOUCHED_RESERVED     (unchanged)
V002_SEALED_TEST           = UNTOUCHED_RESERVED     (unchanged)
HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE (unchanged)
test_rows_loaded           = 0                      (preserved)
```

No evidence reserve was opened, read, listed for content, enumerated, sampled, scored, spent, proposed, or
recommended. The evidence-budget ledger was not modified and no transition row was added.

## 9. Confirmation that no local artefact was inspected

Confirmed. Nothing under `D:\Prometheus\data\microstructure\` or `D:\Prometheus\data\research\` was
opened, read, listed for content, sampled, parsed, hashed, inspected, scored, or summarized. The Phase
4bn-BB v002 local artefact root and the Phase 4bn-AZ v001 local artefact root were not inspected. No
Parquet, research JSON, prediction file, manifest sidecar, or generated target was opened. **No row-level
prediction was inspected.**

## 10. Confirmation that no code, test, model, or research runner was executed

Confirmed. No market-data builder, research runner, diagnostic, replay, model, bootstrap, or backtest was
run. `pytest`, Ruff, and mypy were not run — the phase is docs-only and the mandate forbids them. No
project script, label or feature pipeline, or runtime process was executed. No metric was computed,
recomputed, or reinterpreted. Only `git` bookkeeping, read-only repository document reads, and permitted
read-only external documentation retrieval occurred.

## 11. Candidate counts

```text
Candidate families considered:                18
Candidate families rejected:                  16
Candidates surviving for independent review:   2
```

Surviving candidates, in neutral identifier order:

```text
NL-C1  Price-only effective-spread estimation for the admissible substrate
NL-C2  Perpetual-futures funding mechanism as a no-arbitrage friction bound
```

No candidate is selected, ranked, recommended, or preferred. The permitted range for surviving candidates
was 0 through 5; zero remained a live outcome until the final admissibility pass, and the strongest case
for `SELECT_NONE__REMAIN_PAUSED` is recorded in full at main report §17.

The sixteen rejections are recorded in the mandatory negative-search log (main report §9) with, for each:
family name, external mechanism source considered, nearest Prometheus prior family, reason for rejection,
and the named ground — `DUPLICATION`, `INADMISSIBLE_DATA`, `WEAK_IDENTIFICATION`, `RESEARCHER_FREEDOM`,
`ABSENT_DECISION_CONSEQUENCE`, `COST_DISPROPORTIONALITY`, or `GOVERNANCE_CONFLICT`.

## 12. Exact result state

```text
CANDIDATE_SHORTLIST_PRODUCED__INDEPENDENT_FABLE_REVIEW_REQUIRED__NO_LANE_SELECTED
```

## 13. Commit SHA

Per the project's standard self-reference convention, this closeout is committed together with the main
report in the phase's single commit, so the commit SHA cannot be embedded in the file it names. The
authoritative record is:

```text
branch: phase-4bn-be/external-theory-new-lane-discovery-admissibility-shortlist
commit: the single commit created by this phase, message
        "research(phase-4bn-be): assess external-theory new-lane candidates"
base:   fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0
```

The exact SHA is reported in the final operator report and is recoverable from
`git log --oneline fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0..HEAD`.

## 14. Working-tree state

After commit, the working tree carries only the permitted transient untracked
`.claude/scheduled_tasks.lock`. No tracked file is modified, staged, or deleted. `git diff --check`
reports no whitespace or conflict-marker error over the base-to-tip range. The base-to-tip diff shape is
exactly two `A` entries, zero `M`, zero `D`, zero `R`.

No destructive Git operation was used at any point: no `reset`, no `stash`, no `clean`, no `rebase`, no
`amend`, no force push, no hook bypass, and no history rewriting.

## 15. Merge non-authorization

**No merge is performed and no merge is authorized by this phase.** No merge-closeout is created. `main`
is untouched. The phase is **branch-complete**, not project-complete; per
`docs/00-meta/process/phase-workflow-standard.md`, a phase is project-complete only after its
merge-closeout is recorded on `main`. A merge requires separate operator review and a separately
authorized merge prompt.

## 16. Successor non-authorization

**No successor phase is authorized.** No preregistration, M0 phase, data-acquisition phase, reserve-spend
proposal, model, implementation, or execution phase is proposed, drafted, scoped, or authorized. No
successor prompt was created. `Phase 4bn-BD` was not reused, redefined, or created, and remains what
Phase 4bn-BC recorded it as: the title of a rejected continuation.

This phase did not begin, and must not be read as beginning, an independent review, a merge phase, an M0
phase, a data-acquisition phase, or any other successor work.

## 17. Independent Fable review requirement

Because candidates survive, an **independent Fable review is required** before either candidate could
become a proposed lane. The self-contained, neutral review packet is main report §19.

Conditions carried from `docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md`
§15 and from the Phase 4bn-AW / Phase 4bn-AX precedent:

- the reviewer must be **distinct from this execution agent**;
- a **fresh reviewer chat**, with the literal no-inspection instruction, no repository access, and no
  attached project handoff;
- the bounded packet is the entire evidence set;
- **one task in the first round**; critique and any phase-design work belong to separate later rounds;
- an incomplete or context-limited review does **not** satisfy the requirement and must not be treated as
  if it did;
- the review is **advisory and non-binding**. It cannot authorize a candidate, a phase, data access, or a
  reserve spend. Only the human operator can authorize anything, and only through a separately authorized
  docs-only M0 phase thereafter.

**Fable was not invoked during Phase 4bn-BE.**

## 18. Preserved locks and states

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED`; `CF1_VALID_PASS` as a development-level forecast result
only; `R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED`; strategy M0 `NOT_CLEARED`; the fact that
`M0.2` / `M0.8` / `M0.12` `PASS` is **not** partial pre-clearance; `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
`V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`; `V002_SEALED_TEST = UNTOUCHED_RESERVED`;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`;
`research_eligible = false`; `eligibility_gate_status = pending`; all authorization flags false; the Phase
4aw always-raising `flip_research_eligible(...)` behaviour (never invoked); the Phase 4bn-AE §19 absolute
strategy / PnL / backtest boundary; the Phase 4ak twelve-clause M0 gate with its §6 post-null cooldown
rule and §7 cooled-down-family list; the locked 8 bps per side / 16 bps round trip; the Phase 4bn-BB and
Phase 4bn-AZ no-rerun boundaries; the retained verdict ledger (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, the
5m thread, V2, G1, C1); every dataset identity and hash; all split, holdout, sidecar, and storage
policies; the evidence-ledger statuses; and the reserve spending-authority rules.

**No stopped arc is softened, merged, reinterpreted, reopened, or rescued.** No Prometheus scientific
value is computed, recomputed, reinterpreted, narrowed, or softened by this phase.

## 19. Exact non-authorization statements

```text
Phase 4bn-BE selects no new research lane and authorizes no successor phase.
```

```text
Any surviving candidate requires an independent Fable review, an operator decision, and a separately authorized docs-only M0 phase before it can become a proposed lane.
```

```text
No market data, local research artefact, evidence reserve, model, signal, strategy, backtest, PnL, paper, shadow, live, or exchange-write activity is authorized by Phase 4bn-BE.
```

```text
Remaining paused is a valid outcome.
```

## 20. Recommended operator action

Review the two Phase 4bn-BE files and the final operator report, then decide separately whether to
authorize a merge phase. No merge is performed or authorized here and no merge-closeout is created.

Because candidates survive, the next possible step after a merge decision would be an independent Fable
review under §17 conditions, followed by an operator decision. Neither is authorized by this phase.

`Remaining paused is a valid operator choice.`
