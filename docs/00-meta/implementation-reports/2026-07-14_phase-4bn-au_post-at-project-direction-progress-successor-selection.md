# Phase 4bn-AU — Post-AT Project-Direction Review and Progress-Successor Selection

## 1. Phase name, branch, base SHA, phase type, risk tier

- **Phase name:** Phase 4bn-AU — Post-AT Project-Direction Review and Progress-Successor Selection.
- **Branch:** `phase-4bn-au/post-at-project-direction-progress-successor-selection`.
- **Base SHA:** `6ba589bc704e06f28ba30039aff8ead6523c5031` (`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AT merge-closeout SHA-finalization commit).
- **Phase type:** Docs-only project-direction review, independent-review assessment, provisional successor recommendation, and bounded successor scoping. **Not** an implementation, research-execution, data, model, strategy, backtest, replay, or operational phase. It inspects committed documentation, committed source, committed tests, and Git metadata only, and creates documentation only.
- **Risk tier:** Tier 1 (Full Phase) under `docs/00-meta/process/phase-risk-tiering-standard.md` — it touches scientific direction, evidence-reserve reasoning, and the successor-selection decision, so it is treated at the highest ceremony tier even though it mutates no eligibility, manifest, verdict, or lock. It **records a recommendation only**; it changes no authorization state.

This memo distinguishes three tiers of status precisely: **recommended next direction** (recorded here), **proposed future phase** (Phase 4bn-AV, scoped but not created here), and **authorized work** (remains false; nothing is authorized). Only the first two are recorded.

## 2. Exact repository state and authority hierarchy

**Repository state at branch time (verified before branching):**
- `git status --short` → only `?? .claude/scheduled_tasks.lock` (transient; not staged, modified, deleted, or committed).
- `HEAD == main == origin/main == 6ba589bc704e06f28ba30039aff8ead6523c5031`.
- No unexpected tracked modification; no unexpected untracked item.
- `data/microstructure/` and `data/research/` remain gitignored local namespaces; not opened, read, enumerated, staged, or committed.

**Authority hierarchy applied (highest first):**
1. Committed repository evidence at the base SHA.
2. Specialist documents for their own domain.
3. Recent implementation reports / closeouts / merge-closeouts for recent phase history, decisions, exact evidence, and authorization boundaries.
4. Committed source and tests for actual implemented behavior.
5. Process standards under `docs/00-meta/process/`.
6. `docs/00-meta/current-project-state.md` as a historical/navigational summary only where current.
7. README as non-authoritative for current state unless corroborated.
8. Chat handoffs and independent-review opinions as secondary continuity/critique only.

`docs/00-meta/current-project-state.md` is **stale**: its narrative ends at approximately Phase 3k (post-D1-A consolidation, remain-paused), and the entire Phase 4 series — the local-safe runtime foundation (4a–4e), the microstructure acquisition arc (4as–4bb), and the full 4bn ML/top-of-book arc (4bn-AH…AT) — is absent from it. The authoritative recent state is the Phase 4bn implementation-report series and committed code/tests, which govern where they conflict with the summary.

## 3. Exact Phase 4bn-AS and Phase 4bn-AT stop decisions and why they differ

- **Phase 4bn-AS decision:** `STOP_LONGHORIZON_ML_ARC`. The pre-v002 aggTrades-only long-horizon (5m/30m/1h) directional-ML line is stopped because the clean 15s majority-floor win **inverted** at longer horizons (5m accuracy uplift vs majority −0.222 pp; 30m −1.348 pp; 1h −2.868 pp), the 5m calibration is unusable (≥0.8 tail 0.497 below the 0.512 majority floor), block evidence is mixed (23/45 dates, 1/2 months), and — decisively — the pre-v002 holdout is now **consumed**, so any same-data follow-up would be result-informed rescue with high multiple-testing risk while the only admissible confirmation would burn a scarce one-shot reserve to confirm a sub-threshold, non-actionable signal. The frozen evidence did not justify continuation and post-hoc rescue risk was unacceptable.

- **Phase 4bn-AT decision:** `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`. The docs-only execution of the deferred Phase 4bn-AK §16(b) `bookticker_midprice_data_admissibility_memo` — a **model-free** measurement-validity question (was the clean 15s last-trade result genuine midpoint movement or bid–ask bounce?). It is stopped because **no currently-admissible retrospective source can answer it** (the futures um daily bookTicker archive exists on `data.binance.vision` but is Tier-1-undocumented, carries an unremediated out-of-order defect (issue #305, closed no-fix), reportedly ceased updating in 2024, and its coverage of the required 2024-10-02…2024-11-30 window is unconfirmed from Tier-1 index metadata), **while prospective capture is regime-non-comparable and cannot be aligned to the 2024 aggTrades** under examination, so it does not answer the specific question — at real cost and with rescue/relitigation risk, for low decision-relevant information gain.

**Why the two stops are distinct (they must not be merged into one generic failure statement):**
- The **long-horizon ML arc** stopped because the **frozen evidence did not justify continuation** and **post-hoc rescue risk was unacceptable** — an *evidence-and-methodology* stop on a fully-executed experiment.
- The **top-of-book mechanism arc** stopped because **no currently admissible retrospective source could answer the question, while prospective capture would not be regime-comparable to the historical result** — a *source-admissibility / measurability* stop on a question that was never executed against data.

One is "we ran it and it did not clear the bar, and rescuing it would be dishonest"; the other is "we cannot honestly run it at all on available data." Both preserved every prior lock; neither reopened the other.

## 4. Exact no-successor and capability-authorization posture

- **No successor execution is currently authorized.** Phase 4bn-AT's recorded result state is `TOP_OF_BOOK_MECHANISM_ADMISSIBILITY_MEMO_MERGED_TO_MAIN__STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE_RECORDED__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`.
- All published authorization flags remain `false`; `research_eligible = False`; `eligibility_gate_status = PENDING`; the Phase 4aw `flip_research_eligible(...)` invariant remains permanently-raising and is never invoked.
- Every downstream capability (data acquisition/read, feature/label construction, diagnostics, ML training/scoring, strategy specification, signal generation, PnL/Sharpe/backtest/replay/simulated fills, paper/shadow/live/exchange-write, authenticated APIs/private endpoints/WebSockets/MCP/Graphify/`.mcp.json`) remains unauthorized, each behind the absolute Phase 4bn-AE §19 M0 boundary and its own separate authorization.

## 5. Consumed-holdout and scarce-reserve status

- The **pre-v002 predictive holdout** (14 dates, 2024-11-17…2024-11-30) is **consumed** (scored under Phase 4bn-AR). It must never be described as untouched, unseen, sealed, independent confirmation, or reusable confirmation evidence; it may be used only for descriptive decomposition, and only if a future admissible decomposition ever occurs.
- The **v002 terminal window** (2024-12-01…2025-02-28) and the **sealed test split** (2025-02-14…2025-02-28, `test_rows_loaded = 0`) remain **scarce one-shot reserves**, genuinely unseen. This phase does not read, load, inspect, score, enumerate, or otherwise consume them.

## 6. Project locks preserved

All preserved unchanged by this phase:
- `STOP_LONGHORIZON_ML_ARC` — final for the completed long-horizon ML arc.
- `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` — final for the assessed top-of-book source situation.
- Phase 4aw `flip_research_eligible(...)` — permanently-raising; not invoked or weakened.
- `research_eligible = False`; `eligibility_gate_status = PENDING`; all published authorization flags `false`.
- Phase 4bn-AE §19 M0 boundary — absolute; locked economic context 8 bps/side · 16 bps round-trip binding and descriptive; future quoted-spread evidence prospective-only.
- All completed strategy verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A; 5m / V2 / G1 / C1 threads) and retained-evidence classifications.
- Phase 4bb-F sidecar policy, Phase 4bn-L storage/budget policy, split policies, dataset identities, hashes, and prior reports.

## 7. Repository files and code/test/governance areas inspected

**Decision-lineage memos and closeouts (read directly):**
- `2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md` (61 sections), `..._phase-4bn-at_merge-closeout.md`, `..._phase-4bn-at_closeout.md`.
- `2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md` (35 sections), and the AS closeout/merge-closeout.
- `2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md` (the four `CONTINUE_FOLLOWUP_CATEGORIES`; the `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP` decision; §16(b) `bookticker_midprice_data_admissibility_memo` "deferred, not foreclosed").
- Phase 4bn-AJ / AP / AQ / AR reports and closeouts as restated through AK/AS/AT.

**Governance / process / meta:**
- `docs/00-meta/m0-mechanism-admissibility-gate.md` (twelve-clause M0 gate §5; post-null cooldown §6; §7 cooled-down families).
- `docs/00-meta/decision-framework.md`; `docs/00-meta/current-project-state.md` (stale, navigational only).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ab_source-admissibility-memo.md`, `..._4bn-y_chronological-split-holdout-policy.md`, `..._4bn-ae_ml-baseline-preregistration-contract-amendment.md`, `..._4bn-aa_pre-v002-split-policy-artefact.md`, `2026-06-01_phase-4bn-l_derived-stack-storage-budget-memo.md`.
- `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`.
- Process standards under `docs/00-meta/process/` (phase-workflow, phase-risk-tiering, merge-closeout, operator-report).

**Runtime/safety source and tests (Candidate A audit):**
- `src/prometheus/events/` (`envelope.py`, `runtime_events.py`), `execution/fake_adapter.py`, `operator/state_view.py`, `persistence/runtime_store.py`, `state/` (`control.py`, `mode.py`, `transitions.py`, `errors.py`), `core/governance.py`, `core/errors.py`, `risk/` (`exposure.py`, `sizing.py`, `stop_validation.py`, `errors.py`), `cli.py`.
- `tests/unit/runtime/` (`test_fake_adapter.py`, `test_runtime_persistence.py`, `test_runtime_end_to_end.py`, `test_operator_state_view.py`, `test_runtime_state.py`, `test_runtime_events.py`, `test_governance_labels.py`, risk skeleton tests).
- Phase 4a-era runtime-foundation reports: `2026-04-30_phase-3x_phase-4a-safe-slice-scoping.md`, `..._phase-4a_local-safe-runtime-foundation.md`, `..._phase-4d_runtime-foundation-review-and-next-slice-decision.md`, `..._phase-4e_reconciliation-model-design-memo.md`, and the 4a/4b/4c closeouts.

**Committed source constants (read, not modified):** `src/prometheus/research/microstructure/manifest.py` (`research_eligible = False`; `flip_research_eligible` always raises), `pre_v002_ml_dataset_contract.py` (locked 8/16 bps; frozen success thresholds), `pre_v002_split_policy.py`, `pre_v002_fixed_baseline_run.py` (fail-closed sealed/terminal guards), `canonical_paths.py`.

No file under `data/` was opened. No source, test, script, config, or prior report was modified. No script, test, builder, diagnostic, model, backtest, or runtime process was executed. No network call or external source was used (the supplied Fable review was operator-provided; no external review was requested).

## 8. Current strategy-independent runtime/safety capability inventory (what already exists)

From static reading of committed source and tests:
- **Runtime state model & invariant enforcement — EXISTS.** `state/mode.py` (`RuntimeMode`: SAFE_MODE/RUNNING/BLOCKED/EMERGENCY/RECOVERY_REQUIRED), `state/control.py` (frozen `RuntimeControlState`; `fresh_control_state()` = SAFE_MODE, entries blocked), `state/transitions.py` (pure transitions; `enter_running` rejects illegal predecessors and every blocking flag; `clear_kill_switch` returns to SAFE_MODE, preserves operator_review). Fail-closed validators at multiple boundaries.
- **Runtime persistence — EXISTS (partial hardening).** `persistence/runtime_store.py` (SQLite, WAL, `synchronous=FULL`, single-row UPSERT, append-only `runtime_mode_event` / `governance_label_audit` tables, idempotent `initialize`, corrupt-mode fail-closed on load). No secrets persisted.
- **Event contracts — EXISTS (defined, not yet dispatched).** `events/envelope.py` (`MessageEnvelope`, deterministic id), `events/runtime_events.py` (mode-changed, kill-switch, fake-exchange-lifecycle with `is_fake=True` invariant, governance-label events).
- **Deterministic fake exchange — EXISTS (bounded).** `execution/fake_adapter.py` (`FakeExchangeAdapter`; in-memory; injectable clock; no real-exchange imports, no credentials, no I/O; entry→fill→stop→trigger lifecycle; unknown-outcome and stop-submission-failure paths).
- **Operator read-only observability — EXISTS (complete).** `operator/state_view.py::format_state_view` (pure, read-only) + `cli.py inspect-runtime --db PATH` (no mutating subcommand); test-verified to expose no action verbs.
- **Runtime governance labels — EXISTS.** `core/governance.py` (StopTriggerDomain, BreakEvenRule, EmaSlopeMethod, StagnationWindowRole; `is_fail_closed`, `require_valid`, `parse_*`). (Note: this is runtime *label* governance, not epistemic/evidence-budget governance.)
- **Risk skeletons — EXISTS (in-scope subset).** `risk/exposure.py` (exposure gate; Rules 7/9 partial by design), `risk/sizing.py` (stop-distance sizing; locked live constants exposed), `risk/stop_validation.py` (stop predicates gated by stop-trigger domain).

## 9. Designed-but-unimplemented runtime/safety inventory (what is missing)

- **Reconciliation engine (intended-vs-actual/fake divergence detection) — ABSENT.** No `reconciliation` module. `RuntimeMode.RECOVERY_REQUIRED` and `enter_recovery_required` exist as a state with no workflow. Fully specified but unbuilt in `2026-04-30_phase-4e_reconciliation-model-design-memo.md` (13-class taxonomy, 11 fail-closed boundaries, I/O contracts, `reconciliation_event` table). Deliberately second-in-line: it cannot be meaningfully tested until the fake adapter can *produce* divergence.
- **Deterministic fake-exchange divergence/failure injection — PARTIAL.** `fake_adapter.py` injects only unknown-outcome and stop-submission failure; `FakeOrderOutcome.REJECTED` is defined but never emitted. Missing: partial fills, disconnect/stale-state, orphaned/multiple stops, side/size mismatch, cancel-and-replace (the Phase 4e §18 minimal set).
- **Restart re-hydration hardening — PARTIAL, with a concrete latent defect.** The documented restart-safety invariant (never auto-resume RUNNING after a crash; reconstruct fresh SAFE_MODE carrying forward only kill-switch/review/incident/pause) is enforced **only in test code** (`test_runtime_end_to_end.py`, `test_runtime_persistence.py`), not in any production function. `RuntimeStore.load_persisted()` is inspection-only; there is no `rehydrate_on_startup(...)`.
- **Runtime audit-log export + defensive redaction — ABSENT.** Audit rows are written but no export/dump API and no redaction layer exist (Phase 4d §9.2 Option B, never authorized).
- **Generic control-state invariant checker — ABSENT.** `UnknownStateError` / `EntriesBlockedError` are defined as fail-closed hooks but never raised; no load-time checker rejects internally-inconsistent flag combinations (e.g., RUNNING with kill_switch_active).

**Verdict:** Candidate A's "one exact missing strategy-independent safety slice" premise **holds**; multiple qualifying slices exist, the cleanest standalone fake/local-testable one being the restart re-hydration correctness fix (c), with fake-exchange divergence injection (b) as the enabler for reconciliation (a).

## 10. Existing epistemic / evidence-budget governance inventory

Strongly present and binding, but scattered:
- **M0 twelve-clause mechanism-admissibility gate** (`m0-mechanism-admissibility-gate.md`, Phase 4ak) + **post-null cooldown** (§6) — upstream pre-hypothesis admissibility; anti-rescue (M0.10); rejection-topology distance (M0.4); cost realism at 8/16 bps (M0.5); data-feasibility declaration incl. "unavailable → blocking" (M0.8); prospective-only; authorizes nothing.
- **Preregistration machinery** (Phase 4bn-AE) — claim scope (§8), dependence policy (§10), metric registry (§13), calibration/cost policy (§14/§15), success/continue/kill criteria (§16), ambiguous handling (§17), **finite arc budget + stopping rule** (§18), absolute §19 strategy/PnL/backtest boundary.
- **Split / holdout / sealed-reserve structure** (Phase 4bn-Y) — pre-v002 214/45/14 chronological split; sealed test (single-use, `test_rows_loaded=0`, seven prohibited uses); v002-terminal by-reference-only; required multiple-testing log (§19); code-enforced boundary (`pre_v002_split_policy.py`).
- **Source-admissibility vocabulary** (Phase 4bn-AB) — layered admissibility (contract-design vs data-read vs builder vs ML/diagnostics authorized), separated from manifest flags.
- **Anti-rescue reasoning executed in practice** (Phase 4bn-AS §21/§24; Phase 4bn-AT §43–§48) — garden-of-forking-paths analysis; consumed-holdout constraint; scarce-reserve status appendices.
- **Storage budget** (Phase 4bn-L) — 300 GiB derived-stack hard cap; 500/350 GiB free-space floor; 20 fail-closed stop conditions (incl. "any attempt to read sealed test data"). Governs *disk*, not *evidence*.
- **Code-enforced invariants** — manifest immutability (`flip_research_eligible` always raises; `research_eligible=False`); split-boundary hard-exclusion of v002 terminal + sealed test; per-run sealed/terminal-untouched proof (`test_rows_loaded=0`); locked cost constants and frozen success thresholds.

## 11. Material governance gaps, if any

Three narrow but genuinely-absent binding mechanisms (not merely "scattered restatements"):
1. **No standing evidence-budget / scarce-reserve LEDGER.** The remaining reserves (v002 terminal window; sealed test; consumed pre-v002 holdout) are named and their status described, but only ad hoc inside individual phase memos and re-derived each time; there is no consolidated inventory and no cumulative *consumption record* of what reserve was spent when. (The only artifact literally called a "ledger" is the unrelated retained-verdict ledger.)
2. **No named reserve-spending AUTHORITY or binding pre-spend review.** The only authority is the generic operator; independent review (ChatGPT, external, Fable) is explicitly advisory and non-binding; no quorum/two-person/independent-sign-off requirement gates spending a one-shot reserve.
3. **No LATE-inadmissibility-discovery consequence rule.** Governance is strong at *pre-execution* fail-closed gating (Phase 4bn-L stop conditions; Phase 4bn-AT `DATA_INTEGRITY_FAILURE` precedence), but there is no protocol for what happens if a source is found inadmissible *after* a result was produced and relied upon (no verdict-revision/rollback/quarantine/reserve-refund rule).

These are decision-control / evidence-budget mechanisms genuinely missing in committed form — the basis on which Candidate E can be non-duplicative. All other epistemic substance (M0, preregistration, anti-rescue, cooldown, multiple-testing, restart conditions) already exists; re-legislating it would be duplicative and is out of scope for any admissible E.

## 12. Duplicate / already-complete items excluded

Excluded from candidacy because already implemented or already governed:
- Operator read-only observability (e) — complete (`state_view.py` + CLI).
- Event/state invariant enforcement (f) for the implemented state set — present (`transitions.py` guards; load-time corrupt-mode rejection).
- M0 gate, preregistration, anti-rescue, cooldown, multiple-testing discipline, split/holdout/sealed-reserve structure, source-admissibility timing, restart conditions after stops — all already binding; an E that restated them would be rejected as duplicative.
- Storage budget (Phase 4bn-L) — complete for disk.
- Manifest immutability / eligibility locks — complete and code-enforced.

## 13. Faithful summary of the supplied Fable review

Operator-supplied, bounded, non-binding. Recorded in full in the companion assessment file; compact form:
- **Ranking:** A > B > D > C. **Primary recommendation:** A — local-only, strategy-independent safety/runtime infrastructure.
- **Rationale for A:** does not depend on a market-edge claim; consumes no predictive holdout, sealed reserve, disputed data, or new hypothesis; fully distant from both stopped arcs; fake/local failure-injection and reconciliation testing can be bounded and falsifiable; defects found would have direct future decision consequences.
- **Strongest objection to A:** runtime infrastructure may become scaffolding for a system with no viable strategy; deployment-shaped artifacts may create sunk-cost pressure toward paper/shadow/live.
- **Clean kill criterion for A:** the selected component must have a written, strategy-agnostic acceptance test executable entirely with fake local state; kill if satisfying it requires real/historical market data, network, credentials, exchange-write semantics, or a particular strategy's behavior.
- **Evidence that would change Fable's ranking:** (1) a scoping pass proving no relevant safety/runtime component is genuinely missing; (2) the high-level project record materially misstating evidence reserves, authority hierarchy, or restart conditions.
- **Additional option E** — Forward-Looking Epistemic Protocol and Evidence-Budget Governance (codify binding pre-authorization rules; preregister hypotheses/stopping rules; account for sealed reserves; define who may authorize scarce-evidence use and under what conditions; decide source admissibility before execution; reduce late-inadmissibility discovery; docs-only, strategy-independent). Fable's view: E is distinct from B (B consolidates past state; E changes future authorization decisions) and "could contend with A for first place."

## 14. Critical assessment of Fable's reasoning against repository evidence

- **A's premise (a component is genuinely missing) — CONFIRMED by repository audit.** Reconciliation (a) is absent; fake-exchange divergence injection (b) is partial; restart re-hydration (c) has a concrete latent defect (invariant enforced only in test code); audit-export/redaction (d) is absent. Fable's condition (1) that would *lower* A ("no component is genuinely missing") is therefore **not met** — A stays viable.
- **Fable's strongest objection to A — CORROBORATED and load-bearing.** The project is paused with no authorized strategy and two stopped arcs; runtime infrastructure is genuinely off the critical path, so "scaffolding for a system with no viable strategy" and deployment-shaped sunk-cost drift are real, unrefuted risks. This objection weighs materially against A here.
- **Fable's clean kill criterion — sound and adopted verbatim in substance** for any A-shaped AV (see §21).
- **Fable's condition (2) — partially bears on E, not A.** The high-level record (`current-project-state.md`) *is* materially stale (ends ~3k), but the reserves, authority, and restart conditions are correctly recorded in the recent 4bn memos, which are authoritative; so the staleness is navigational, not a misstatement that changes reserve or authorization facts. This is a point for B/E housekeeping, not a reason to distrust the record.
- **Fable's Candidate E — CONFIRMED partially additive.** The repository audit shows E's substance largely already exists (M0, AE, Y, AS/AT), but three genuine holes remain (ledger, named authority/quorum, late-inadmissibility rule, §11). Fable's framing that "E changes future authorization decisions while B consolidates past state" is accurate. Fable's own uncertainty ("E could contend with A for first place") is well-founded.
- **Where Fable is incomplete / audit-dependent:** Fable ranked A #1 without the repository scoping pass that this phase performed; that pass both *confirms* A's premise and *sharpens* the decisive counter — the missing runtime slice is a **latent, non-current** risk (the runtime is dormant), whereas the evidence-governance gap is a **live, next-step** risk that directly guards the project's scarcest irreplaceable asset. That distinction, unavailable to Fable, is what tips the provisional decision.

Fable authorizes nothing; it is weighed against the committed record, not followed automatically.

## 15. Candidate set A–E

- **A — Local-only, strategy-independent safety/runtime infrastructure** (one exact bounded slice, e.g. restart re-hydration (c), fake-exchange divergence injection (b), or reconciliation (a)).
- **B — Repository current-state and negative-results consolidation** (refresh the stale high-level state, stopped-arc map, evidence-reserve map, authority index, restart conditions).
- **C — Genuinely unrelated hypothesis-discovery memo** (docs-only, ex-ante mechanism distant from both stopped arcs and all rejected families; no data, no strategy spec).
- **D — Strategy-independent measurement/data-feasibility memo** (a measurement question whose admissibility is provable before any data read; not a disguised top-of-book reopening).
- **E — Forward-Looking Epistemic Protocol and Evidence-Budget Governance** (docs-only; ledger + named spending authority/quorum + source-admissibility timing + late-inadmissibility rule + restart conditions; must not re-legislate existing standards).

"Remain paused" is the existing burden-of-proof baseline only, and is **not** an eligible winner because the operator requested progress.

## 16. Scoring framework (defined before scoring)

Every candidate is scored on the same criteria using a bounded integer scale **1–5** (1 = poor / high-risk-or-cost; 3 = neutral/moderate; 5 = strong / low-risk). Higher is better throughout (for risk-type criteria, "5" means *low* risk). Equal weights; the arithmetic total is a **sanity check only** — the decision is governed by the decisive A-vs-E question (§19) and the ordered tie-breakers, not by the sum. Weights are not tuned to force any candidate.

Criteria (C1–C16):
- C1 novelty / distance from stopped/rejected work
- C2 mechanism or governance clarity
- C3 data admissibility (5 = no data needed / clearly admissible)
- C4 independence from scarce untouched evidence (5 = consumes none)
- C5 low post-hoc rescue risk
- C6 low multiple-testing / researcher-degrees-of-freedom risk
- C7 falsifiability / clean kill criterion
- C8 value of a negative/null result
- C9 decision consequence
- C10 low engineering/data/documentation burden
- C11 durable project value independent of eventual strategy success
- C12 compatibility with M0 and current authorization boundaries
- C13 low risk of rhetorical/sunk-cost drift toward paper/shadow/live
- C14 ability to remain local-only/fake-only/network-free/credential-free/exchange-write-free
- C15 low duplication of already-completed functionality or governance
- C16 clean bounded completion condition

## 17. Candidate-by-candidate assessment

**A — safety/runtime slice (scored on the cleanest slice, restart re-hydration (c)).**
Premise holds (§9). Strong on admissibility (no data), scarce-evidence independence, falsifiability/clean-kill (a crisp fake/local acceptance test), local-only purity, durable value, and bounded completion. Weaknesses: it addresses a **latent, non-current** risk (the runtime is dormant, nothing is authorized to run it, so the defect cannot manifest while paused); it carries real deployment-shaped sunk-cost drift risk (Fable's strongest objection); and its decision consequence is a correctness hardening rather than a change to any live decision. Low novelty is acceptable (it is engineering, not hypothesis work).

**B — current-state / negative-results consolidation.**
The high-level summary is genuinely stale (ends ~3k). But the staleness is **navigational, not decision-critical**: every recent 4bn phase re-derives state from the authoritative report series and explicitly flags the summary as stale, and the reserves/locks/verdicts are correctly recorded in those memos. So B does not close a *material* decision or evidence-consumption gap; the risk of a wrong decision or accidental evidence consumption from the stale summary is low. B also overlaps with E's consolidation-index component. Useful housekeeping; not the strongest progress path.

**C — fresh unrelated hypothesis-discovery memo.**
Legitimate forward progress and squarely M0's domain, docs-only. But it is the **highest-novelty-risk** option: it must find a genuinely new mechanism outside the rejection topology (R2/F1/D1-A/V2/G1/C1) and both stopped arcs, which the project has repeatedly found depleting; and even a good hypothesis immediately hits the same evidence-budget and source-admissibility cliffs that E addresses — so C is premature before those cliffs are governed. High researcher-degrees-of-freedom risk if not tightly gated.

**D — strategy-independent measurement/data-feasibility memo.**
Concrete and potentially admissible-before-data. But it sits **dangerously close to the just-stopped top-of-book measurement work (AT)**: it would carry a high risk of being read as a disguised reopening of the microstructure/ToB measurement line, and any admissible measurement question would again confront the evidence-budget/admissibility governance E provides. Weaker now than E for the same "premature before governance" reason as C, and with added reopening-adjacency risk.

**E — forward-looking epistemic protocol and evidence-budget governance.**
Premise holds for a **tightly-scoped** version (§11): three genuinely-absent binding mechanisms (ledger, named authority/quorum, late-inadmissibility rule) plus a consolidated index. Strong on admissibility (no data), scarce-evidence independence, M0 compatibility, zero deployment/sunk-cost drift, and decision consequence (it gates the spending of the project's scarcest irreplaceable asset and is live at the very next research step). Weaknesses: much of the *surrounding* epistemic substance already exists, so scope discipline is essential to avoid duplication; and governance-writing carries an "endless-loop" / low-tangibility risk that must be bounded by a hard completion condition. When scoped to the three holes + index, it is non-duplicative, bounded, and closes the more material current risk.

## 18. Comparative score / rank table

Scale 1–5, higher better; equal weight; total is a sanity check only.

| Criterion | A (slice c) | B | C | D | E |
|---|---|---|---|---|---|
| C1 novelty/distance from stopped/rejected | 3 | 2 | 4 | 3 | 4 |
| C2 mechanism/governance clarity | 5 | 4 | 2 | 3 | 4 |
| C3 data admissibility (none needed) | 5 | 5 | 5 | 4 | 5 |
| C4 independence from scarce evidence | 5 | 5 | 4 | 4 | 5 |
| C5 low post-hoc rescue risk | 5 | 5 | 3 | 3 | 5 |
| C6 low multiple-testing / DoF risk | 5 | 5 | 3 | 3 | 5 |
| C7 falsifiability / clean kill | 5 | 3 | 3 | 4 | 4 |
| C8 value of a negative/null result | 3 | 2 | 3 | 3 | 3 |
| C9 decision consequence | 3 | 2 | 3 | 3 | 5 |
| C10 low burden | 4 | 4 | 4 | 3 | 4 |
| C11 durable value independent of strategy | 5 | 3 | 2 | 3 | 5 |
| C12 M0 / boundary compatibility | 5 | 5 | 4 | 3 | 5 |
| C13 low paper/shadow/live drift risk | 2 | 5 | 4 | 3 | 5 |
| C14 local/fake/network-free/etc. | 5 | 5 | 5 | 4 | 5 |
| C15 low duplication of existing work | 5 | 3 | 4 | 3 | 4 |
| C16 clean bounded completion | 5 | 4 | 3 | 3 | 4 |
| **Total (max 80)** | **70** | **62** | **56** | **52** | **72** |
| **Rank** | **2** | **3** | **4** | **5** | **1** |

The totals place **E (72)** marginally ahead of **A (70)**, with B/C/D clearly behind. The A-vs-E margin is small, consistent with a genuine judgment call; the decision is made on the decisive question and tie-breakers below, not the two-point arithmetic gap. My ranking (E > A > B > C > D) revises Fable's (A > B > D > C) by promoting E to first and A to second (Fable's first), which is consistent with Fable's stated uncertainty that "E could contend with A for first place."

## 19. Explicit A-versus-E decision analysis

**A eligibility test (all must hold):** (1) one exact component genuinely absent/materially incomplete — **YES** (restart re-hydration (c): the documented restart-safety invariant is enforced only in test code, not production). (2) not already implemented by a later phase — **YES** (no production `rehydrate_on_startup`). (3) predeclared fake-local acceptance test — **YES** (persist RUNNING+kill-switch → simulate restart → assert SAFE_MODE, kill-switch carried, entries blocked). (4) requires no market data/network/credentials/exchange-write/strategy assumptions — **YES**. (5) value even if no viable strategy is ever found — **YES**. (6) scope does not imply paper/shadow/live readiness — **mostly YES** (it hardens crash-recovery of the operator control state, but still lives in the deployment-adjacent runtime). (7) smaller and more decision-useful than a broad runtime program — **YES**. **A is eligible.**

**E eligibility test (all must hold):** (1) a material evidence-budget/authorization gap exists — **YES** (ledger, named authority/quorum, late-inadmissibility rule). (2) existing governance does not already close it — **YES for those three holes** (existing docs cover the surrounding substance but not these). (3) would change future authorization decisions rather than summarize — **YES** (it gates spending the sealed test / v002 terminal and defines late-inadmissibility consequences). (4) writable without designing a new strategy/hypothesis — **YES**. (5) defines enforceable preconditions, not aspirational prose — **YES** (a ledger, a named-authority + pre-spend-review gate, a late-discovery consequence rule are enforceable process preconditions). (6) bounded completion — **YES** (one document covering the three holes + index). (7) no endless governance-writing loop — **YES if scoped and forbidden from re-legislating M0/AE/AS/Y**. **E is eligible.**

**Both are eligible, so apply the decisive question:** *Which option closes the more material current project risk while preserving the strongest future ability to find and honestly test a strategy?*

- The **runtime/safety gap (A)** is a **latent, non-current** risk: the runtime is dormant, nothing is authorized to run it, and the rehydration defect cannot manifest until the runtime is actually started against a real or paper exchange — many gates away (a viable strategy, M0, backtest, dry-run, paper), none of which exist. Real, worth fixing, but off the current critical path, and carrying deployment-shaped sunk-cost drift risk.
- The **evidence-governance gap (E)** is a **live, next-step** risk: the operator has chosen forward progress, and the moment any new research line opens, the first questions are exactly "what may we spend, who authorizes spending the sealed test, is this rescue, what if the source proves inadmissible after reliance." E guards the project's scarcest, irreplaceable asset (the last unseen v002 terminal + sealed test) with binding mechanisms that are genuinely absent today, and it is precisely what "preserves the strongest future ability to find and honestly test a strategy" means.

Both halves of the decisive question favor **E**: it closes the more material *current* risk (the epistemic/evidence domain is live; the runtime is dormant) and it most directly preserves the future ability to honestly test a strategy. The existing governance's two recent successes (AS refusing a scarce-reserve spend; AT catching inadmissibility before acquisition) were **hand-rolled each time** — institutionalizing them removes dependence on that diligence recurring, which is added value, not duplication.

**Provisional winner: Candidate E.** A is the strong runner-up.

## 20. Exactly one provisional winner

**Provisional successor direction: Candidate E — Forward-Looking Epistemic Protocol and Evidence-Budget Governance.**

Provisional recommendation state: `RECOMMEND_FORWARD_LOOKING_EPISTEMIC_PROTOCOL_AND_EVIDENCE_BUDGET_SUCCESSOR`.

This is a **recommended next direction** and a **proposed future phase** only. It is **not** authorized work.

## 21. Proposed Phase 4bn-AV title and bounded scope

**Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending Authority, and Late-Inadmissibility Consequence Protocol (docs-only).**

- **Phase type:** Docs-only governance-authoring phase. Creates exactly one new governance document plus its own closeout; modifies no existing file. No data, model, strategy, backtest, or acquisition work.
- **Precise problem statement:** The project holds scarce, irreplaceable one-shot evidence (v002 terminal window; sealed test split; a now-consumed pre-v002 holdout) and a strong-but-scattered epistemic ruleset, yet has **no standing ledger** of those reserves and their consumption, **no named spending authority or binding pre-spend independent-review/quorum** gate, and **no rule for what happens if a source is found inadmissible after a result was relied upon.** AV would close exactly those three gaps and add a consolidated index pointing to (without altering) the existing scattered rules.
- **Why distinct from both stopped arcs:** It reopens neither the long-horizon aggTrades ML arc nor the top-of-book mechanism arc; it proposes no hypothesis, target, feature, model, threshold, horizon, or data source; it reads and spends **no** evidence. It is forward-looking governance about *how future evidence may be spent*, not a re-run or rescue of any prior result.
- **Exact allowed actions:** read committed docs/source/tests/Git metadata; author one new governance document defining (1) an evidence-budget & scarce-reserve **ledger** (standing inventory of remaining reserves + a consumption-event record format); (2) a named **spending authority** for one-shot reserves plus a binding pre-spend independent-review/quorum precondition; (3) a **late-inadmissibility-discovery consequence rule** (verdict/reserve/quarantine handling if a source is found inadmissible after reliance); (4) a **consolidated index** pointing to existing standards (M0, AE, Y, AB, AS, AT) without restating or amending them; (5) explicit **restart conditions** for future research after repeated stops, by reference to M0 §6, not by rewriting it. Commit documentation only.
- **Exact forbidden actions:** re-legislating, amending, or duplicating M0's twelve clauses, Phase 4bn-AE preregistration machinery, Phase 4bn-AS anti-rescue reasoning, or Phase 4bn-Y split/holdout policy; modifying any existing governance, process, or state file; any strategy/hypothesis/signal/PnL/backtest/replay work; any data acquisition/read/feature/label/model/diagnostic; reading/enumerating/scoring the v002 terminal or sealed test; any manifest/gate/sidecar/split/eligibility/authorization-flag change; invoking or weakening `flip_research_eligible(...)`; authorizing the spending of any reserve (it defines the *process*, spends nothing); network/credentials/private endpoints/MCP/Graphify/`.mcp.json`.
- **In-scope files/areas:** one new file under `docs/00-meta/` (e.g. an evidence-budget-governance document) plus its closeout under `docs/00-meta/implementation-reports/`. Read-only reference to the existing governance corpus.
- **Explicitly out-of-scope:** all source, tests, scripts, configs, manifests, gates, sidecars, splits, datasets, models; `current-project-state.md` and all existing governance/process/M0 files (no modification); any `data/` content.
- **Entry prerequisites:** separate ChatGPT review of these AU files; explicit operator authorization; a new Claude Code prompt. `research_eligible` remains false; all authorization flags remain false.
- **Acceptance criteria:** one new governance document exists that (i) enumerates the remaining scarce reserves and defines a consumption-record format; (ii) names a spending authority and a binding pre-spend review/quorum precondition for one-shot reserves; (iii) defines the late-inadmissibility consequence rule; (iv) indexes (not restates) the existing standards; (v) states restart conditions by reference; and demonstrably adds no content that duplicates M0/AE/AS/Y.
- **Kill / stop criteria (binding, Fable-derived in substance):** kill AV if authoring it requires re-legislating existing M0/AE/AS/Y machinery (i.e., the only content would be duplication → the gap was not real → STOP); kill if the ledger/authority/late-rule cannot be defined without designing a new strategy, hypothesis, or data source; kill if it degenerates into an open-ended governance-writing loop with no bounded completion; kill if it would require touching data, code, the manifest, or any existing governance file. (The A-shaped kill criterion — kill if the acceptance test requires market data, network, credentials, exchange-write semantics, or strategy assumptions — is recorded here for completeness and would bind an A-shaped AV instead.)
- **Expected evidence output:** the new governance document + closeout; no metrics, no data, no model outputs.
- **Tests required:** none — docs-only; no executable file changes.
- **Local generated state permitted:** none.
- **Value even if the project never reaches paper or live:** the protocol protects the project's only remaining irreplaceable confirmation evidence from accidental or rescue-motivated consumption and institutionalizes the honest-testing discipline that any future research must satisfy — value that is entirely independent of whether a viable strategy is ever found.
- **Strongest counterargument (against AV):** see §24.
- **Conditions that would overturn the recommendation before authorization:** see §25.

## 22. Why the winner is not a rescue or reopening of stopped work

Candidate E proposes **no** hypothesis, target, feature, horizon, threshold, model, or data source; it reads and spends **no** evidence; it reinterprets **no** prior verdict; it touches neither stopped arc. It is forward-looking governance about *how future evidence may be spent and how source admissibility is timed and remediated* — the opposite of reviving `STOP_LONGHORIZON_ML_ARC` or `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`. It cannot function as post-hoc rescue because it produces no result to rescue and defines constraints, not experiments.

## 23. Why it does not cross M0, strategy, PnL, backtest, paper, shadow, live, or exchange-write boundaries

AV is docs-only and authorizes nothing. It defines process preconditions that sit *upstream* of M0 and *upstream* of any strategy/PnL/backtest/paper/shadow/live/exchange-write path; it strengthens, and never relaxes, the Phase 4bn-AE §19 M0 boundary. It creates no code, no signal, no simulated fill, no exchange interface, and no eligibility transition. All published authorization flags and `research_eligible` remain false.

## 24. Strongest counterargument against the winner

The strongest case against E, and for promoting A instead: **E's surrounding substance already exists and "worked twice" (AS refused a scarce-reserve spend; AT caught inadmissibility before acquisition), so the three remaining holes are preventive of a hypothetical future mis-spend rather than an acute present harm — whereas A's restart re-hydration slice is a concrete, falsifiable, provably-missing safety defect (an invariant enforced only in test code) with a perfect fake/local acceptance test.** A skeptic can fairly argue that a paused project writing more governance is the seductive substitution of motion for progress — it produces no new capability and no new knowledge — while a bounded safety bug-fix at least leaves the committed codebase measurably better and cleanly satisfies Fable's clean-kill criterion. This counterargument is serious and is the reason A is ranked a close second, not dismissed. It does not prevail because (a) the runtime defect is latent and off the current critical path while the evidence-governance gap is live at the next research step; (b) E's three holes are genuinely-absent binding mechanisms, not restatements, so E is not "rules that already exist"; (c) A carries deployment-shaped sunk-cost drift that E lacks; and (d) protecting irreplaceable evidence outranks hardening a dormant subsystem under the decisive question.

## 25. Conditions that would overturn the recommendation

Before AV is authorized, the recommendation should flip (most plausibly to Candidate A, slice (c)) if any of the following holds:
- ChatGPT or the operator judges the three governance holes low-consequence *while the project is paused and no reserve spend is imminent*, and prefers the concrete, falsifiable safety fix now.
- A concrete new research line is about to open that would actually exercise the runtime, making the restart-safety defect a current rather than latent risk.
- A closer reading shows the three E holes are in fact already covered adequately by an existing document not surfaced in this audit (in which case E collapses to duplicative B-style consolidation and A wins).
- The operator prefers the smallest, most tangible bounded deliverable and explicitly accepts the deployment-shaped-drift risk, subject to the Fable clean-kill criterion.
- A scoping pass on AV shows the ledger/authority/late-rule cannot be written without re-legislating M0/AE/AS/Y (E's own kill criterion) — in which case AV should not proceed and A becomes the successor.

## 26. Explicit negative-result value

If AV, once authorized, finds that the three purported holes are already adequately governed by existing committed standards, that null finding is itself valuable: it converts a scattered, implicitly-adequate ruleset into a proven-adequate one, records the negative result, and cleanly stops (kill criterion) — sparing the project from building governance it does not need and re-pointing the operator to Candidate A. Either outcome (protocol written, or gap disproven) improves the project's decision-control posture.

## 27. Explicit decision consequence

The AU decision determines which single bounded, non-pause, non-reopening phase the operator reviews next. Selecting E means the next reviewable proposal is a docs-only protocol that guards the project's last irreplaceable evidence and institutionalizes honest-testing discipline before any new research line opens; it changes the *future* decision of whether/how the sealed test and v002 terminal may ever be spent, and by whom. Selecting A instead would harden a latent safety defect in the dormant runtime. The AU memo changes no live authorization; it changes only which proposal is next in the queue.

## 28. Independent-review status string

`POST_AT_INDEPENDENT_REVIEW_PROVIDED__FABLE_RANKING_A_GT_B_GT_D_GT_C__CANDIDATE_E_RAISED`

## 29. Required ChatGPT / operator review sequence before AV authorization

1. Operator returns the three AU files (this memo, the Fable independent-review assessment, and the closeout) plus the operator report to ChatGPT for compliance review and plain-language interpretation.
2. ChatGPT reviews the A-vs-E analysis, the scoping of proposed Phase 4bn-AV, and the overturn conditions (§25), and gives an independent (non-binding) opinion.
3. The operator makes a **separate merge decision** for Phase 4bn-AU.
4. Only if the operator then explicitly authorizes Phase 4bn-AV — via a **new** Claude Code prompt — does AV begin. This memo does not create that prompt and does not authorize AV.

## 30. Exact no-successor-execution statement

**No successor execution is authorized by Phase 4bn-AU.**

## 31. Exact phase result state

`POST_AT_PROJECT_DIRECTION_REVIEW_RECORDED__RECOMMEND_FORWARD_LOOKING_EPISTEMIC_PROTOCOL_AND_EVIDENCE_BUDGET_SUCCESSOR__FABLE_INDEPENDENT_REVIEW_ASSESSED__NO_SUCCESSOR_EXECUTION_AUTHORIZED`

## 32. Recommended next operator action

Return the three Phase 4bn-AU files and the operator report to ChatGPT for compliance review, plain-language interpretation, and a separate merge decision. Do not authorize Phase 4bn-AV, generate its execution prompt, or spend any evidence until a separate operator prompt does so explicitly. The project remains paused with respect to execution; this phase records a recommended direction only.
