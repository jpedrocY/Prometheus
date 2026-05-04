# Phase 4z Closeout

## Summary

Phase 4z authored the **Post-Rejection Research-Process Redesign Memo** (docs-only) on branch `phase-4z/post-rejection-research-process-redesign`. Phase 4z is the project's first post-rejection research-process redesign memo, authored after the cumulative six-failure-mode rejection ledger (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness; C1 fires-and-loses / contraction anti-validation) reached a point where the operator authorized a docs-only examination of the *process itself* rather than another fresh-hypothesis discovery cycle. Phase 4z is the Phase 4y §"Operator decision menu" Option B conditional secondary alternative; the operator separately authorized Phase 4z on the conditional-secondary path. **Phase 4z is text-only.** Phase 4z's proposed redesigns are **recommendations** for any future research-process memo, not adopted governance changes. No new strategy candidate was created or named; no fresh-hypothesis discovery memo was authored; no strategy-spec or backtest-plan memo was authored; no backtest was run; no Phase 4x rerun occurred; `scripts/phase4x_c1_backtest.py` was NOT modified; no implementation code was written; no data was acquired or modified; no manifest was modified; no retained verdict was revised; no project lock was changed; no governance file was amended. Whole-repo quality gates remain clean (ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files). **No successor phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4z_post-rejection-research-process-redesign.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4z_closeout.md                                  (new; this file)
```

No source under `src/prometheus/` modified. No tests modified. No scripts modified. No data, manifests, governance files, or `.gitignore` modified. No `current-project-state.md` change (Phase 4z is preserved on its feature branch and is not merged).

## Process-redesign conclusion

The Phase 4y consolidation memo recorded the C1 hard reject and recommended remain-paused as primary with a docs-only research-process redesign memo as conditional secondary. The operator authorized Phase 4z on the conditional-secondary path. Phase 4z's central observation is that the project's strategy-research process is **procedurally sound** (predeclaration discipline, branch isolation, no governance leakage, forbidden-input enforcement, cost realism, variant-grid / DSR / PBO / CSCV discipline, negative-baseline framework at C1, opportunity-rate floors at C1, consolidation-memo discipline) but **substantively under-constrained at the discovery and admissibility layer** — the Phase 4m 18-requirement validity gate and Phase 4t 10-dimension scoring matrix correctly filter for "is this a hidden rescue?" and "is this operationally implementable?" but do not adequately filter for "is this candidate's core thesis substantively novel and theoretically grounded against its closest unconditioned baseline?". The G1 → C1 sequence revealed the gap; both candidates were predeclared, disciplined, and tested cleanly, and both terminated at Verdict C HARD REJECT. Phase 4z's proposed redesigns target this gap with a 32-item proposed admissibility framework, a design-family-distance matrix (F-1 / F-2 / F-3 / F-4), an explicit M0 theoretical-admissibility gate, an explicit edge-rate viability gate distinct from the opportunity-rate viability gate, and predeclared-baseline-superiority-from-theory requirements at the hypothesis-admissibility layer. Phase 4z's redesigns are recommendations only; adoption is a separate operator decision.

## Relationship to Phase 4y

- Phase 4y merged the Post-C1 Strategy Research Consolidation Memo into `main` at SHA `69579c15f4ddc15cf79edbf22a67daa84a43f765` with housekeeping at SHA `8e94fb01951e07d428046026750f20197dfe9890`.
- Phase 4y recommendation: Option A — remain paused (primary); Option B — docs-only post-rejection research-process redesign memo (conditional secondary; not started by Phase 4y).
- The operator separately authorized Phase 4z on the conditional-secondary path.
- Phase 4z is docs-only.
- Phase 4z does NOT modify any prior governance.
- Phase 4z's proposed redesigns are recommendations; Phase 4z does NOT amend the Phase 4m 18-requirement validity gate, Phase 4t 10-dimension scoring matrix, Phase 4u opportunity-rate principle, Phase 4w negative-baseline / PBO / DSR / CSCV methodology, Phase 4j §11 metrics OI-subset rule, Phase 4k V2 backtest-plan methodology, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 3r §8, §11.6, or §1.7.3.
- Phase 4z does NOT modify `scripts/phase4x_c1_backtest.py` or rerun the backtest.
- Phase 4z does NOT use Phase 4l / 4r / 4x forensic numbers as tuning input.
- Phase 4z does NOT authorize Phase 5 / Phase 4aa / any successor phase.

## Six-failure topology recap

| # | Strategy | Failure mode | Evidence layer | Process implication Phase 4z observes |
| --- | --- | --- | --- | --- |
| 1 | **R2** | Cost-fragility | Mechanism generated; cost survival failed (§11.6 HIGH blocks) | Cost-survival must be a primary-design constraint, predicated on first-principles theoretical content. |
| 2 | **F1** | Catastrophic-floor / bad full-population expectancy | Mechanism generated; M3 PASS-isolated only | Mechanism subset PASS is research evidence; full-population PASS is the binding promotion criterion. |
| 3 | **D1-A** | Mechanism / framework mismatch | M1 BTC h=32 PASS; framework cond_i / cond_iv FAIL | Mechanism PASS does not imply framework PASS; both must be predeclared and met. |
| 4 | **V2** | Design-stage incompatibility | 0 trades (CFP-1 critical) | Setup geometry / stop / target / sizing must be co-designed; V1-inherited filters cannot be passively re-imposed. |
| 5 | **G1** | Regime-gate-meets-setup intersection sparseness | 0 qualifying trades (CFP-1 + CFP-9 independent) | Multi-condition AND classifiers naturally produce sparse intersections; joint event rate must be predeclared from theory. |
| 6 | **C1** | **Fires-and-loses / contraction anti-validation** | 149 trades; multi-baseline anti-validation (M1 -0.244R CI [-0.41, -0.08]; M2.a -0.220R CI [-0.39, -0.06]; M2.b -0.293R) | Opportunity-rate viability ≠ edge-rate viability; baseline-superiority must be predeclared from theory with bootstrap-CI pass criterion. |

Six categorically distinct failure modes; the project's strategy-research record now carries terminal rejections in three orthogonal evidence layers (zero-trade non-evidence-generating; full-population evidence-generating expectancy failure; multi-baseline anti-validation).

## What worked in the research process

11 components preserved verbatim:

1. Strict docs-first sequence (hypothesis → strategy-spec → backtest-plan → backtest-execution → consolidation → discovery).
2. Branch isolation per phase.
3. No premature implementation (Phase 4a runtime is strategy-agnostic).
4. No live path (no paper / shadow / live; no production keys; no exchange-write).
5. Explicit project locks preserved (§11.6, §1.7.3, mark-price stops, Phase 3r / 3v / 3w / 4j §11 governance) across six rejection events.
6. Backtest plans before execution (Phase 4k / 4q / 4w predeclared methodology).
7. Forbidden-input enforcement (audit-zero CFP-10 / CFP-11 / CFP-12 across V2 / G1 / C1 executions).
8. Negative baselines binding at C1 (Phase 4w M1 / M2.a / M2.b framework).
9. Opportunity-rate floors at C1 (CFP-9 binding; rate 3.33 / 480 bars).
10. PBO / DSR / CSCV discipline at C1 (Bailey & López de Prado 2014; CSCV S=16, C(16,8)=12,870 combinations; no silent approximation).
11. Merge closeouts and current-project-state synchronization at every merge.

## What failed in the research process

Six observations (process gaps; not corrections to existing governance):

1. Repeated candidate ideas clustered around the "mechanical condition + breakout" design family (V2, G1, C1).
2. Discovery did not sufficiently penalize design-family adjacency.
3. Theory-to-baseline superiority was under-specified before C1.
4. Fresh-hypothesis gates did not require enough proof that the core condition should outperform a same-geometry unconditioned baseline.
5. Process allowed substantial effort (each Phase 4n/4t→4o/4u→4p/4v→4q/4w→4r/4x arc) on theoretically weak edges.
6. Remain-paused was treated as a boundary but not converted into a stronger discovery-process reset until now (Phase 4z is the first instance).

## Proposed future admissibility framework

Phase 4z proposes a 32-item admissibility framework (A1–A32) that **includes the Phase 4m 18-requirement gate verbatim** (preserved with strengthening notes only) plus **9 proposed new items**:

- A5 design-family declaration (F-1 / F-2 / F-3 / F-4 or new) with distance-from-prior-rejections argument;
- A7 regime-gate / entry-rule / sample-size-viability co-design (G1 lesson);
- A9 explicit causal / mechanistic thesis with named mechanism;
- A10 expected baseline differential Δ_R from theoretical content;
- A12 expected edge-rate from theoretical content (separate from A11 opportunity-rate);
- A13 expected failure mode if hypothesis is wrong (predicted ex-ante);
- A15 sample-size viability from theoretical content;
- A31 closest-prior-failure comparison and how this candidate's failure mode would differ;
- A32 remain-paused-comparison (under what evidence would remain-paused dominate this candidate?).

The framework is a **recommendation** for any future research-process memo, not adopted governance.

## Proposed future discovery memo template

Phase 4z proposes a 23-section discovery memo template (recommendation only) that augments the Phase 4n / Phase 4t structure with: per-candidate design-family declaration; theoretical mechanism statement; predicted baseline differential; predicted opportunity-rate; predicted edge-rate; predicted failure-mode; cost-survival thesis; sample-size viability; design-family-distance matrix; and edge-rate viability analysis as a section distinct from opportunity-rate viability analysis.

## Proposed future strategy-spec changes

Phase 4z proposes 6 strategy-spec template additions (recommendation only): closest baseline definitions before thresholds; "why condition beats baseline" clause; edge-rate floor separate from trade-count floor; rescue-adjacency table; forbidden threshold provenance section; expected failure-mode declaration.

## Proposed future backtest-plan changes

Phase 4z proposes 6 backtest-plan template additions (recommendation only): baseline tables binding (not optional); baseline differential CI required; strategy can fail with positive raw mean_R if baseline outperforms; edge-rate gates separate from CFPs; all post-failure tuning prohibited; methodology amendment forbidden mid-execution.

## Proposed future execution-report changes

Phase 4z proposes 5 execution-report template additions (recommendation only): baseline superiority summary before headline mean_R; failure-mode classification using six-mode topology; forensic-number non-reuse warning; rescue-prohibition summary; process-lessons section.

## Recommended next operator choice

- **Option A — primary recommendation: remain paused.**
- **Option B — conditional secondary: docs-only documentation-refresh / governance-template update memo (only if separately authorized; not started by Phase 4z).** This option would adopt a subset of Phase 4z's proposed redesigns through a separately authorized governance-update phase.
- Option C — docs-only fresh-hypothesis discovery memo NOT recommended (would likely repeat the V2 / G1 / C1 pattern unless redesigns are first adopted or explicitly declined).
- Option D — docs-only strategy-agnostic implementation-readiness scoping memo NOT recommended (binding constraint is strategy evidence, not infrastructure).
- Option E — REJECTED: any C1 / V2 / G1 / R2 / F1 / D1-A rescue.
- Option F — REJECTED: immediate new strategy spec / backtest / implementation / data acquisition.
- Option G — FORBIDDEN: paper / shadow / live / exchange-write / Phase 4 canonical / production keys / MCP / Graphify / `.mcp.json` / credentials.
- Option H — FORBIDDEN: merging Phase 4z to main without explicit operator instruction.

**Phase 5 / Phase 4aa / any successor phase are NOT authorized by Phase 4z.**

## Commands run

```text
git status                                          (clean except gitignored)
git rev-parse main                                  8e94fb01951e07d428046026750f20197dfe9890
git rev-parse origin/main                           8e94fb01951e07d428046026750f20197dfe9890
git checkout -b phase-4z/post-rejection-research-process-redesign
                                                    Switched to new branch
.venv/Scripts/python --version                      Python 3.12.4
.venv/Scripts/python -m ruff check .                All checks passed!
.venv/Scripts/python -m pytest -q                   785 passed (no regressions)
.venv/Scripts/python -m mypy                        Success: no issues in 82 source files
git add docs/00-meta/implementation-reports/2026-04-30_phase-4z_post-rejection-research-process-redesign.md
git commit -F .git/PHASE_4Z_COMMIT_MSG              Phase 4z memo committed (cb426b1)
git push -u origin phase-4z/post-rejection-research-process-redesign
                                                    Branch pushed; tracking origin
```

## Verification results

```text
ruff check .                : All checks passed!
pytest                      : 785 passed (no regressions)
mypy strict                 : Success: no issues in 82 source files

Phase 4z memo line count    : 793 lines (single new file)

No source code modified.
No tests modified.
No scripts modified.
No data acquired or modified.
No manifests modified.
No governance files modified.
No v003 created.
No retained verdicts revised.
No project locks changed.
```

## Commit

```text
Phase 4z memo commit:
  SHA: cb426b127c8fce41e00f9c0684f4d4d7269b82d8
  Title: phase-4z: post-rejection research-process redesign memo (docs-only)
  Files: docs/00-meta/implementation-reports/2026-04-30_phase-4z_post-rejection-research-process-redesign.md (new; 793 lines)

Phase 4z closeout commit:
  SHA: <recorded after this file is committed>
```

## Final git status

```text
On branch phase-4z/post-rejection-research-process-redesign
Untracked files (gitignored transients only):
  .claude/scheduled_tasks.lock
  data/research/
nothing added to commit but untracked files present
```

## Final git log --oneline -5

Recorded after the closeout commit and push.

## Final rev-parse

```text
HEAD                                                              <recorded after closeout commit>
origin/phase-4z/post-rejection-research-process-redesign          <recorded after closeout push>
main                                                              8e94fb01951e07d428046026750f20197dfe9890 (unchanged)
origin/main                                                       8e94fb01951e07d428046026750f20197dfe9890 (unchanged)
```

## Branch / main status

- Phase 4z branch: `phase-4z/post-rejection-research-process-redesign` (created from main; pushed to origin).
- main / origin/main: `8e94fb01951e07d428046026750f20197dfe9890` (unchanged; Phase 4z has not been merged).
- No merge to main is performed by Phase 4z (per authorization brief).

## Forbidden-work confirmation

Phase 4z did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- run `scripts/phase4x_c1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- modify `docs/00-meta/current-project-state.md`, `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist governance file;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 5 / Phase 4aa / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- use Phase 4l / 4r / 4x forensic numbers as tuning input or threshold derivation for any proposed redesign;
- merge Phase 4z to main.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal; preserved)
G1                  : HARD REJECT (Phase 4r terminal; preserved)
C1                  : HARD REJECT (Phase 4x terminal; preserved by Phase 4y)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x / 4y
                            : all preserved verbatim
Phase 4z                    : Post-rejection research-process redesign memo
                              (this phase; new; docs-only; not merged;
                              proposes recommendations only)
Recommended state           : remain paused (primary);
                              docs-only documentation-refresh / governance-
                              template update memo (conditional secondary;
                              not authorized by Phase 4z)
```

## Next authorization status

```text
Phase 5 / Phase 4aa / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
User stream / WebSocket            : NOT authorized
Exchange-write capability          : NOT authorized
MCP / Graphify                     : NOT authorized
.mcp.json / credentials            : NOT authorized
C1 implementation                  : NOT authorized; terminal-rejected
C1 rerun                           : NOT authorized; terminal-rejected
C1 spec amendment                  : NOT authorized; FORBIDDEN
Phase 4w methodology amendment     : NOT authorized; FORBIDDEN
Phase 4m gate amendment            : NOT authorized; recommendations only
Phase 4t matrix amendment          : NOT authorized; recommendations only
Phase 4u opportunity-rate
  principle amendment              : NOT authorized; recommendations only
G1 / V2 / R2 / F1 / D1-A rescue    : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes       : NOT authorized; FORBIDDEN
V2-prime / V2-variant              : NOT authorized; FORBIDDEN
C1-prime / C1-extension            : NOT authorized; FORBIDDEN
Retained-evidence rescue           : NOT authorized; FORBIDDEN
5m strategy / hybrid               : NOT authorized; not proposed
ML feasibility                     : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                   : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                   : NOT authorized; FORBIDDEN
Fresh-hypothesis discovery memo    : NOT authorized; would require
                                     separate operator authorization
Strategy-spec memo                 : NOT authorized; would require
                                     separate operator authorization
Backtest-plan memo                 : NOT authorized; would require
                                     separate operator authorization
Backtest-execution phase           : NOT authorized; would require
                                     separate operator authorization
Implementation-readiness scoping
  memo                             : NOT authorized; not recommended
Documentation-refresh / governance
  -template update memo            : NOT authorized; conditional
                                     secondary in operator decision menu
Phase 4z merge to main             : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
Adoption of Phase 4z proposed
  redesigns as governance          : NOT authorized; recommendations only
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4z to main and adopt a subset of its proposed redesigns through a separately authorized governance-update phase, or take some other action. Until then, the project remains at the post-Phase-4y consolidation boundary on `main` with Phase 4z preserved on its feature branch (not merged).

---

**Phase 4z is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. Phase 4z's proposed redesigns are recommendations for any future research-process memo, not adopted governance. main remains unchanged at 8e94fb0. C1 first-spec remains terminally HARD REJECTED. Recommended state: remain paused. No next phase authorized.**
