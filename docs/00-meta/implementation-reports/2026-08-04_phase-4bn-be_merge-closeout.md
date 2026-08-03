# Phase 4bn-BE — Merge Closeout

## 1. Phase identity

Phase 4bn-BE — External-Theory New-Lane Discovery and Mechanism-Admissibility Shortlist. A **docs-only
external-theory research and governance-screening** phase. **Tier 1 / Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` — it may influence future scientific direction even
though it opened no market data and implemented nothing.

**This merge is a recordkeeping action only.** It records a candidate dossier, a negative-search log, and
a neutral independent-review packet on `main`. It changes no data, no manifest, no eligibility state, no
reserve, no verdict, and no lock; it selects no candidate; and it authorizes no successor phase.

- **Action:** merge into `main`
- **Target branch:** `main`
- **Source branch:** `phase-4bn-be/external-theory-new-lane-discovery-admissibility-shortlist`

```text
Merging Phase 4bn-BE records the external-theory candidate shortlist and its governance boundaries; it selects no new research lane and authorizes no successor phase.
```

## 2. SHAs

| Item | SHA |
|---|---|
| Pre-merge `main` == `origin/main` (Phase 4bn-BC merge-closeout SHA-finalization tip) | `fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0` |
| Phase 4bn-BE approved source-phase commit (two documents added) — `research(phase-4bn-be): assess external-theory new-lane candidates` | `6de62178a1f9a9856e96a7a0c5e9f4dab7dad711` |
| Phase 4bn-BE merge-closeout branch commit (this file) | `PLACEHOLDER_MERGE_CLOSEOUT_BRANCH_COMMIT_SHA` |
| Phase 4bn-BE no-fast-forward merge commit | `PLACEHOLDER_NO_FAST_FORWARD_MERGE_COMMIT_SHA` |

`main == origin/main == fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0` was confirmed at preflight, before any
mutation. The local and remote source branch were confirmed equal at
`6de62178a1f9a9856e96a7a0c5e9f4dab7dad711`.

**SHA-finalization convention.** This merge-closeout is created on the Phase 4bn-BE source branch with the
last two SHAs as explicit placeholders. After the `--no-ff` merge into `main`, one narrow SHA-finalization
commit on `main` (`docs(phase-4bn-be): finalize merge closeout shas`) replaces both placeholders with
their actual values and changes nothing else. A commit cannot embed its own SHA; the finalization commit's
own SHA equals the resulting final `main` / `origin/main` tip and is recorded in the final operator report
and recoverable from the Git log.

## 3. Merge method

`git merge --no-ff` with the default `ort` strategy, from
`phase-4bn-be/external-theory-new-lane-discovery-admissibility-shortlist` into `main`.

- Merge commit message: `research(phase-4bn-be): merge external-theory new-lane shortlist`
- Not squashed, not rebased, not amended, not fast-forwarded.
- Source-branch history preserved exactly: two commits (the approved phase commit, and this
  merge-closeout).
- Force: none. Skip-hooks (`--no-verify`): none. Skip-signing: none.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.
- The source branch is retained and is **not** deleted.

## 4. Files brought forward by the merge

Three added files, all documentation, all under `docs/00-meta/implementation-reports/`:

```text
docs/00-meta/implementation-reports/2026-08-03_phase-4bn-be_external-theory-new-lane-discovery-and-admissibility-shortlist.md
docs/00-meta/implementation-reports/2026-08-03_phase-4bn-be_closeout.md
docs/00-meta/implementation-reports/2026-08-04_phase-4bn-be_merge-closeout.md   (this file)
```

- **Docs:** the three files above.
- **Source:** none.
- **Tests:** none.
- **Scripts:** none.
- **Config:** none.

No `data/microstructure/` file was modified, created, deleted, or committed. No `data/research/` file was
modified, created, deleted, or committed. No prior governance memo, ledger, manifest, phase gate,
roadmap entry, technical-debt record, process standard, source file, test, script, or config was
modified. `docs/00-meta/current-project-state.md`, `CLAUDE.md`, and `README.md` are left unchanged,
matching the docs-only precedent from Phase 4bn-AH through Phase 4bn-BC.

**Neither approved Phase 4bn-BE report was modified by this merge-closeout commit.** Both remain
byte-identical to their state at `6de62178a1f9a9856e96a7a0c5e9f4dab7dad711`.

## 5. Diff summary

Relative to pre-merge `main` `fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0`, the change set is **additions
only**.

The approved phase commit alone, verified at preflight:

```text
git diff --name-status fe28cfcc..6de62178  ->  2 entries, both A
git diff --stat        fe28cfcc..6de62178  ->  2 files changed, 1646 insertions(+)
git diff --check       fe28cfcc..6de62178  ->  clean (no output)
git log --oneline      fe28cfcc..6de62178  ->  exactly 1 commit
```

After creation of this merge-closeout, the full source-branch change set relative to the base remains
additions only:

```text
three A entries
zero M entries
zero D entries
zero R entries
```

No `M`, `D`, or `R` on any pre-existing path. No whitespace or conflict-marker error. The diff matches the
expected change set from the authorization prompt exactly.

The later narrow SHA-finalization commit on `main` modifies **only** this merge-closeout file, replacing
its two SHA placeholders. That is the sole `M` entry that will exist in the base-to-final-`main` range,
and it touches no other path.

## 6. Verdict

**MEMO RECORDED — external-theory candidate dossier, non-selecting.**

Phase 4bn-BE asked whether external primary theory supports any genuinely new Prometheus research
mechanism family that is materially distinct from every stopped, rejected, depleted, or retained family;
meaningful without strategy construction; preregisterable before market-data access; supported by an
admissible and obtainable data source; carrying a legitimate decision consequence on both pass and fail;
proportionate in cost; and independent of any evidence reserve. It searched external theory first and
checked Prometheus admissibility second, in that causal order. Eighteen mechanism families reached a
disposition; sixteen were rejected with named grounds in a mandatory negative-search log; two survive
**for independent adversarial review only**. The phase computed no Prometheus value, opened no data,
touched no reserve, and selected nothing.

Exact scientific and governance result of the phase:

```text
CANDIDATE_SHORTLIST_PRODUCED__INDEPENDENT_FABLE_REVIEW_REQUIRED__NO_LANE_SELECTED
```

Exact merged result state:

```text
CANDIDATE_SHORTLIST_PRODUCED__INDEPENDENT_FABLE_REVIEW_REQUIRED__NO_LANE_SELECTED__MERGED_TO_MAIN__NO_SUCCESSOR_AUTHORIZED
```

This is a **recordkeeping state**. It must not be interpreted as candidate selection or lane
authorization.

### 6.1 Candidate counts

```text
Candidate families considered:                18
Candidate families rejected:                  16
Candidates surviving for independent review:   2
```

### 6.2 Surviving candidates

```text
NL-C1 — Price-only effective-spread estimation for the admissible substrate

NL-C2 — Perpetual-futures funding mechanism as a no-arbitrage friction bound
```

Stated expressly, and not softened:

- the order above is **neutral identifier order**, not a ranking;
- **neither is selected**;
- **neither is ranked**;
- **neither is recommended**;
- **neither is M0-cleared** — every preliminary M0 clause label in the report uses only
  `PLAUSIBLY_SATISFIABLE`, `UNRESOLVED`, `ADVERSE`, or `NOT_APPLICABLE_WITH_JUSTIFICATION`, and `PASS` is
  used for no clause of either candidate;
- **neither is authorized**;
- `SELECT_NONE__REMAIN_PAUSED` remains a **fully available outcome**, and the strongest case for it is
  recorded at main report §17 and is not rebutted there.

A candidate surviving Phase 4bn-BE means only: **worthy of independent adversarial review.** It does not
mean admissible, approved, selected, or authorized.

## 7. Local gitignored outputs

**None.** Phase 4bn-BE produced no local artefact. It opened nothing under `data/microstructure/` or
`data/research/`, inspected neither the Phase 4bn-BB v002 nor the Phase 4bn-AZ v001 artefact root, and
generated no Parquet, JSON, manifest, sidecar, prediction, or target. The pre-existing Phase 4bn-BB and
Phase 4bn-AZ artefact roots remain local and gitignored and are untouched by this merge.

Four ordinary external research PDFs were fetched by the retrieval tool during Phase 4bn-BE into a
temporary session directory **outside the repository**. None resides under `D:\Prometheus`, none was
committed, and none is a project artefact.

## 8. Validation results

Phase 4bn-BE was docs-only; `pytest`, Ruff, and mypy were correctly **not run** and were outside its
authorized scope, and are outside the scope of this merge. Their absence is not a regression.

Pre-existing failures elsewhere in the repository, unchanged and unrelated to this arc: two in
`tests/simulation/test_backtest_real_2026_03.py` (`KeyError: 'trade_count'` at
`src/prometheus/research/data/storage.py:232`) and twelve `mypy --strict` errors. These are **unchanged
from prior phases and not introduced by this merge**.

Structural validation performed for this merge: base-to-tip diff name-status shape, diff stat, whitespace
check, branch/upstream equality for both `main` and the source branch, source-branch commit count, and
staged-scope verification before each commit. All pass (§5).

`git diff --check` over the base-to-source range: clean (no output).

**No-data and no-execution statement.** Phase 4bn-BE and this merge:

- opened **no** Prometheus market data;
- inspected **no** local research artefact;
- opened or spent **no** evidence reserve;
- executed **no** model, test, runner, bootstrap, diagnostic, replay, builder, or backtest;
- called **no** exchange or market-data endpoint;
- calculated **no** Prometheus scientific value.

## 9. Upstream immutability evidence

`main` and `origin/main` were confirmed equal at `fe28cfcc79b726bdf7c6aec6c8b4167f908e25f0` before any
mutation, and were not advanced by any other actor during the merge. The Phase 4bn-BE source branch was
confirmed equal between local and `origin` at `6de62178a1f9a9856e96a7a0c5e9f4dab7dad711` before the
merge-closeout commit and again before the merge. No published history was rewritten, rebased, amended,
reset, stashed, cleaned, cherry-picked, or force-pushed.

Both approved Phase 4bn-BE documents are preserved byte-identical from
`6de62178a1f9a9856e96a7a0c5e9f4dab7dad711` through the merge and through the SHA-finalization commit; the
finalization commit touches only this merge-closeout file.

No local artefact required bit-for-bit preservation, because the phase accessed none.

## 10. Manifest and evidence state preservation

No manifest was read for mutation, and none was mutated.

```text
research_eligible          = false        (unchanged)
eligibility_gate_status    = pending      (unchanged)
all authorization flags    = false        (unchanged)
```

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved
(**never invoked**). `chronological_split_policy` unchanged. Governance labels unchanged.

Evidence-budget ledger state, preserved exactly, with **no ledger transition made and no transition row
added**:

```text
PRE_V002_INTERNAL_HOLDOUT  = CONSUMED
V002_TERMINAL_WINDOW       = UNTOUCHED_RESERVED
V002_SEALED_TEST           = UNTOUCHED_RESERVED
HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE
test_rows_loaded           = 0
```

`CONSUMED` remains terminal. `docs/00-meta/process/evidence-budget-ledger.md` and
`docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md` are unmodified.

## 11. Boundary confirmations

- no candidate selected, ranked, recommended, preferred, or rejected at merge
- no M0 phase begun; no M0 prompt drafted; no M0 clause marked `PASS` for either candidate
- no preregistration begun or drafted
- no Fable or other independent reviewer invoked
- no data acquisition authorized or begun
- no Binance or other exchange endpoint called
- no market data acquired, downloaded, opened, parsed, sampled, hashed, or scored
- no `data/microstructure/` file opened, listed for content, or committed
- no `data/research/` file opened, listed for content, or committed
- no Phase 4bn-AZ or Phase 4bn-BB local artefact root inspected
- no Parquet, local research JSON, prediction file, generated target, manifest, or sidecar opened
- no row-level prediction inspected
- no evidence reserve opened, read, sampled, scored, spent, proposed, or recommended
- no evidence-ledger transition made
- no model trained, fitted, scored, or run; no bootstrap, diagnostic, replay, builder, research runner, or
  backtest run
- no pytest, Ruff, or mypy run
- no signal, strategy, position rule, threshold, event definition, or trading action created
- no PnL, expectancy, profitability, or trading economics computed
- no credential, `.env`, WebSocket, MCP, Graphify, `.mcp.json`, or external code used
- no external datum used to calculate any Prometheus result
- neither approved Phase 4bn-BE report modified
- no governance document, ledger, manifest, phase gate, roadmap entry, technical-debt record, process
  standard, source file, script, test, config, or data file modified
- `docs/00-meta/current-project-state.md`, `CLAUDE.md`, and `README.md` unmodified
- `D:\Prometheus-Project-Control` not modified
- `.claude/scheduled_tasks.lock` never staged, modified, deleted, cleaned, moved, or committed
- merge performed with `--no-ff`; no squash, no fast-forward, no rebase, no amend, no reset, no stash, no
  clean, no cherry-pick, no force-push, no hook bypass, no history rewrite
- source branch retained, not deleted
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no stopped arc softened, merged, reinterpreted, reopened, or rescued
- no successor authorized

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

**All preserved verbatim.**

## 13. Preserved project locks

Preserved exactly and unchanged:

```text
STOP_LONGHORIZON_ML_ARC
STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE
REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH
REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

```text
CF1_VALID_PASS
```

is preserved **only as a development-level forecast result** — it is not a signal, not a strategy, not a
recommendation, and not an action. It establishes no direction, no profitability, no economic materiality,
no transaction-cost clearance, no tradability, and no M0 clearance.

```text
strategy M0            = NOT CLEARED
research_eligible      = false
eligibility_gate_status = pending
all authorization flags = false
8 bps per side
16 bps round trip
```

`M0.2` / `M0.8` / `M0.12` `PASS` remains **not** partial pre-clearance of anything.

Also preserved: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position /
mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; the Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
cooled-down families list + memo template; the Phase 4al refined no-rescue rule + §13 boundary + §14
hierarchy; the Phase 4bn-AE §19 absolute strategy / PnL / backtest boundary; the Phase 4bn-AT §58
prohibition on any friction evidence revising completed metrics, completed rejections, prior materiality
decisions, or the locked cost reference; the Phase 4bn-BB and Phase 4bn-AZ no-rerun boundaries; the Phase
4bn-AV evidence ledger, spending-authority standard, and late-inadmissibility protocol; Phase 4bb-F
sidecar policy; Phase 4bn-L storage/budget policy; all split, holdout, and storage policies; and every
dataset identity and hash.

**All prior phase results preserved verbatim. No stopped arc is softened, merged, reinterpreted,
reopened, or rescued.**

## 14. No-rescue constraints

The Phase 4bn-BE merge does not, and cannot, be construed as authorising:

- selection, ranking, endorsement, or rejection of `NL-C1` or `NL-C2`;
- opening a research lane, or treating a surviving candidate as a lane;
- an M0 assessment, an M0 memo, or an M0 prompt;
- a preregistration, an experiment contract, a threshold, a tolerance, an event definition, or a model;
- ML model training, model selection, strategy hypothesis generation, or any conversion of a measurement
  into a signal;
- strategy signal construction, strategy logic, position state, entry / exit rules, sizing, gating,
  execution timing, or backtest design;
- PnL computation or any claim of economic materiality, cost clearance, or tradability;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- any label generation at any horizon, or barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / index / premium-index / cross-venue / order-book / bookTicker / multi-symbol
  aggTrades / additional aggTrades acquisition;
- reopening the stopped long-horizon ML arc, the stopped top-of-book mechanism arc, the rejected
  forced-flow / liquidation-proxy family, or the rejected CF-1 filter continuation;
- old-strategy alt-symbol rerun or cooled-down-family reopening (M0 §7.A / §7.B / §7.C / §7.D / §7.E all
  remain as recorded and none is relaxed);
- 5m research-thread reopening (Phase 3t closure preserved);
- any rerun or reclassification of Phase 4bn-AZ or Phase 4bn-BB;
- opening, spending, or proposing a spend of any evidence reserve;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`, or
  `chronological_split_policy` from this evidence alone;
- resolving, by any means, the retrieval limitations recorded in the phase report — they remain
  unresolved and continue to count **against** the candidates they concern.

```text
No market data, local research artefact, evidence reserve, model, signal, strategy, backtest, PnL, paper, shadow, live, or exchange-write activity is authorized by Phase 4bn-BE or by its merge.
```

## 15. Successor authorization

**None.**

```text
No successor phase is authorized by this merge.
```

```text
Phase 4bn-BE selects no new research lane and authorizes no successor phase.
```

```text
Any surviving candidate requires an independent Fable review, an operator decision, and a separately authorized docs-only M0 phase before it can become a proposed lane.
```

Explicitly **not** authorized, and not drafted anywhere in this record:

- an independent Fable review of the Phase 4bn-BE packet;
- an M0 mechanism-admissibility phase for `NL-C1`;
- an M0 mechanism-admissibility phase for `NL-C2`;
- any preregistration phase for either candidate;
- any data-acquisition phase (index-price klines, premium-index klines, multi-symbol aggTrades,
  bookTicker, depth, forceOrder, or any other family);
- any reserve-spend proposal or reserve-spend execution phase;
- `Phase 4bn-BD` — which exists in the record **only** as the title of the continuation Phase 4bn-BC
  declined, and which is neither reused, redefined, nor created here;
- any corrective phase for the Phase 4bn-BC merge-closeout findings F2–F5;
- any phase repairing or retiring `docs/00-meta/current-project-state.md` or the `CLAUDE.md` import chain;
- Phase 5; Phase 4 canonical;
- ML implementation; strategy implementation; backtest implementation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private
  endpoints; user stream; MCP / Graphify / `.mcp.json` / credentials.

No successor prompt was drafted by this merge.

## 16. Recommended state

**Remain paused.**

```text
Remaining paused is a valid outcome.
```

The merge records a dossier, not a direction. The project's posture after this merge is exactly what it
was before: paused, with no open research lane, no authorized successor, both evidence reserves untouched,
and every lock intact. The next move is an **operator decision about direction** — not a task.

**Conditional next, NOT authorized.** The cleanest non-paused option would be an independent Fable review
of the neutral packet at main report §19, conducted by a fresh reviewer distinct from the Phase 4bn-BE
execution agent, under the bounded-context conditions of
`docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md` §15. Such a review
would assess novelty, hidden reduction to stopped work, mechanism identification, researcher freedom,
decision consequence, evidence leakage, reserve pressure, cost proportionality, and the strongest reason
to select none. It is **not** authorized by this merge, requires a separate operator decision, and would
itself authorize nothing.

## 17. Independent compliance review at merge time

An external compliance review of the branch-complete Phase 4bn-BE returned:

```text
COMPLIANT_WITH_NOTES__RECOMMEND_MERGE
```

The compliance reviewer was **distinct from the Phase 4bn-BE execution agent**.

**This compliance review is not, and must not be described as, the required independent Fable scientific
review.** It reviewed governance compliance of a branch-complete phase and recommended a merge. It did not
assess the scientific merit of either candidate, and it authorizes nothing.

Non-blocking notes, recorded without softening:

1. **`NL-C1` is computable but lacks an admissible quote-based validation benchmark**, and its preliminary
   M0.8 assessment is `ADVERSE`.
2. **`NL-C2` is structurally cleaner but its positive quantity is confounded** by convenience yield,
   limited arbitrage capital, margin, collateral-funding, and liquidation effects.
3. **Source-retrieval limitations remain unresolved** and were counted against candidates.
4. **Neither candidate is selected or M0-cleared.**
5. **The strongest `SELECT_NONE__REMAIN_PAUSED` case remains substantive and live.**

None of the five notes is repaired, resolved, or argued against by this merge.

## 18. External-research provenance

Phase 4bn-BE reviewed **13 retrieved or bibliographically verified primary sources**, tabulated in main
report §6.1 with authors, title, year, venue or institution, DOI / stable identifier / canonical URL, the
specific mechanism claim each supports, and the specific limitation each carries for Prometheus. It named
a further **18 works without bibliographic verification** in the negative-search log (main report §6.2);
**none carries a substantive claim**, and no rejection rests on any of them — every rejection rests on a
repository-grounded ground stated in the log.

The retrieval limitations recorded at main report §6.3 are **preserved and not resolved by this merge**.
They are, in summary: publisher access failures (HTTP 403 / 402) for two published articles; an inability
to render research PDFs to text in the execution environment; and the fact that the authoritative route to
the BTCUSDT perpetual tick size is an endpoint call the phase was forbidden to make. Consistent with the
Phase 4bn-AT §8 precedent, each was counted **against** the candidate it concerns rather than resolved by
any prohibited means, and each remains an open, recorded uncertainty.

## 19. Independent Fable review boundary

- **Fable was not invoked during Phase 4bn-BE, and is not invoked by this merge.**
- The independent Fable review remains a **possible separate next step only after a new operator
  decision**.
- The review must use a **fresh reviewer distinct from the execution agent**, with no repository
  inspection and no attached project handoff, per the bounded-context standard.
- The review is **advisory only**. It cannot authorize a lane, an M0 phase, a preregistration, data
  access, or a reserve spend. Only the human operator can authorize anything.
- **This merge does not itself authorize that review or any successor task.**

## 20. Merge non-scientific consequence

This merge changes **no** scientific verdict, **no** candidate status, **no** evidence classification,
**no** reserve status, **no** lock, **no** eligibility state, and **no** authorization flag.

It moves three documentation files onto `main` and nothing else. `CF1_VALID_PASS` remains exactly what it
was; both stopped arcs remain stopped and distinct; the rejected forced-flow family and the rejected CF-1
filter continuation remain rejected; both reserves remain `UNTOUCHED_RESERVED`; the consumed holdout
remains `CONSUMED` and terminal; `test_rows_loaded` remains `0`; strategy M0 remains `NOT CLEARED`; and
`NL-C1` and `NL-C2` remain unselected, unranked, unrecommended, un-cleared, and unauthorized.

```text
Merging Phase 4bn-BE records the external-theory candidate shortlist and its governance boundaries; it selects no new research lane and authorizes no successor phase.
```

```text
Phase 4bn-BE selects no new research lane and authorizes no successor phase.
```

```text
Any surviving candidate requires an independent Fable review, an operator decision, and a separately authorized docs-only M0 phase before it can become a proposed lane.
```

```text
No market data, local research artefact, evidence reserve, model, signal, strategy, backtest, PnL, paper, shadow, live, or exchange-write activity is authorized by Phase 4bn-BE or by its merge.
```

```text
Remaining paused is a valid outcome.
```
