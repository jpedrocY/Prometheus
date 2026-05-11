# Chat Branching Handoff Standard

## Title

Prometheus Chat Branching Handoff Standard — required shape of the
handoff that operator (with ChatGPT) prepares when continuing the
project in a new chat.

## Purpose

This document specifies the shape of the handoff that anchors a new
chat to the current state of the Prometheus repository. It exists to
prevent the most dangerous failure mode of cross-chat work: a new
chat that understands project content but misses the lifecycle state,
the merge-closeout discipline, the local artefact assumptions, or the
forbidden activities, and consequently recommends an unsafe phase.

A well-formed handoff anchors the new chat to repo state with explicit
SHAs, file paths, artefact SHA256s, and instructions to query the
repo before recommending or executing anything. A malformed handoff
relies on chat memory and invites scope drift.

This document is **process-only**. It does not authorize any phase.

## When to branch chat

Branch to a new chat when:

- the current chat has accumulated enough context that responses are
  slow or imprecise,
- a phase merge-closeout has just been recorded and a fresh chat
  would benefit the next phase's debate,
- the operator wants a clean handoff for review continuity,
- the operator is changing implementation focus from one arc to
  another,
- the operator wants to onboard a new ChatGPT thread to the project
  after time has passed.

The default behaviour is **continue in the current chat** when
context is fresh. Branching is for context refresh, not for routine
phase work.

## Required handoff sections

Every chat-branching handoff must contain exactly these 15 sections
in order:

1. **Project identity** — name (Prometheus), one-sentence purpose,
   current arc.
2. **Repository and local path** — repo URL or name, absolute local
   path (`C:\Prometheus`), branch policy (`main` is authoritative;
   working branches use `phase-{X}/{slug}` form).
3. **Current `main` / `origin/main` SHA** — exact short and / or
   full SHA of `main` and `origin/main`. State whether they are in
   sync.
4. **Last completed phase** — phase identifier, phase name, phase
   type, and lifecycle state (must be "merge-closeout recorded" if
   the phase is project-complete; if "branch-complete" only, state
   that explicitly).
5. **Last merge-closeout path** — absolute path to the most recent
   merge-closeout file under
   `docs/00-meta/implementation-reports/`.
6. **Current local data assumptions** — enumerated list of local
   gitignored artefacts that the new chat may assume to exist on the
   operator's machine, with paths and SHA256s. If the new chat
   should not assume any local artefacts exist, state that
   explicitly.
7. **Current artefacts and SHAs** — table of the most relevant
   artefacts: raw manifest, raw zip, raw gate report, normalized
   parquet, derived manifest, derived gate report, successor-state
   JSONs, feature parquet, feature manifest, feature gate report,
   feature successor-state, label parquet, label manifest, with
   SHA256s.
8. **Current arc summary** — one-paragraph summary of the current
   research / implementation arc and which phase boundary the
   project is at.
9. **Phases completed in current arc** — enumerated list of
   merge-closeout-recorded phases in the current arc, with phase
   identifier, name, and merge-closeout path.
10. **Retained verdicts** — full ledger (H0, R3, R1a, R1b-narrow,
    R2, F1, D1-A, 5m thread, V2, G1, C1), each preserved verbatim.
11. **Project locks** — full list (§11.6, round-trip, §1.7.3, Phase
    3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase
    4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase
    4ak M0, Phase 4al refined no-rescue rule).
12. **Current non-authorizations** — enumerated list of forbidden
    activities: ML, strategy, backtests, acquisition, paper / shadow
    / live, deployment, exchange-write, production keys, authenticated
    APIs, private endpoints, user stream, MCP, Graphify, `.mcp.json`,
    credentials, manifest transition, successor phases.
13. **Known validation caveats** — note any pre-existing validation
    failures (e.g. the `KeyError: 'trade_count'` simulation failures
    that have been unchanged since prior phases). State that they
    are unchanged from prior phases and should not be treated as new.
14. **Recommended next phase or paused state** — explicit
    recommendation: "Remain paused" (default) or "Author Phase {Y}"
    with precise scope and rationale.
15. **Ready-to-paste continuation prompt** — a fully formed prompt
    that the operator can paste into the new chat to anchor it to
    repo state. The prompt must include the repo-query requirement.

## Required continuation prompt sections

The ready-to-paste continuation prompt that the operator pastes into
the new chat must contain:

1. **Project identity** — Prometheus, current arc.
2. **Repository and local path** — `C:\Prometheus`.
3. **Current `main` SHA** — exact SHA, with instruction to verify
   `git rev-parse main == git rev-parse origin/main`.
4. **Last merge-closeout path** — instruction to read.
5. **Last phase implementation report path** — instruction to read.
6. **Current local data assumptions** — instruction to verify
   artefact paths and SHA256s exist locally.
7. **Retained verdicts and project locks** — instruction to read
   `docs/00-meta/current-project-state.md`.
8. **Current non-authorizations** — list verbatim.
9. **Recommended next phase or paused state**.
10. **Repo-query requirement** — explicit instruction to query the
    repo before recommending or executing anything.
11. **"Do not rely on this handoff alone" rule** — explicit
    instruction that the handoff is a starting point, not a
    substitute for current repo state.

## Repo-query requirement for new chats

A new chat must, before recommending or executing any phase:

1. **Read `docs/00-meta/current-project-state.md`** and identify the
   current phase block.
2. **Read the most recent merge-closeout** under
   `docs/00-meta/implementation-reports/`.
3. **Read the most recent phase implementation report**.
4. **Confirm `git rev-parse main == git rev-parse origin/main`**.
5. **Confirm whether the latest phase is branch-complete (no
   merge-closeout) or merge-closeout recorded (project-complete)**.
6. **Confirm any local data assumptions** that the candidate next
   phase will rely on (for example, presence and SHA256 of a label
   parquet under `data/microstructure/labels/`).
7. **Confirm retained verdicts and project locks have not silently
   shifted** between summaries.

A new chat that skips this step is unsafe and must be corrected.

## Current-state verification checklist

Before the new chat acts:

- [ ] `git rev-parse main` returns the expected SHA.
- [ ] `git rev-parse origin/main` returns the same SHA.
- [ ] `git status` is clean (or shows only expected untracked items,
      such as `data/research/`).
- [ ] `docs/00-meta/current-project-state.md` reflects the expected
      "Current phase" block.
- [ ] The latest merge-closeout file exists at the expected path.
- [ ] The latest phase implementation report exists at the expected
      path.

## Latest-phase verification checklist

Before recommending a next phase:

- [ ] Last phase identifier matches handoff.
- [ ] Last phase has a merge-closeout (project-complete) or is
      branch-complete (not project-complete).
- [ ] Last phase's successor authorization status is "None".
- [ ] No silent phase has happened that the handoff did not mention
      (i.e. the latest merge-closeout is the one the handoff
      references).

## Merge-state verification checklist

Before recommending a merge prompt or a new phase:

- [ ] `main` is in sync with `origin/main`.
- [ ] No branch is staged for merge that has not been reviewed.
- [ ] No `data/microstructure/` file is staged.
- [ ] No forbidden tracked file is staged.
- [ ] No untracked file appears that should be gitignored.

## Local-data assumptions checklist

If the candidate next phase depends on local artefacts:

- [ ] `data/microstructure/raw/` artefacts exist if needed.
- [ ] `data/microstructure/manifests/` artefacts exist if needed.
- [ ] `data/microstructure/normalized/` artefacts exist if needed.
- [ ] `data/microstructure/features/` artefacts exist if needed.
- [ ] `data/microstructure/labels/` artefacts exist if needed.
- [ ] `data/microstructure/gate-reports/` artefacts exist if needed.
- [ ] `data/microstructure/successor-state/` artefacts exist if
      needed.
- [ ] SHA256s match the values recorded in the handoff and in the
      latest merge-closeout.

If any required local artefact is missing, the next phase must
either:

- be a phase that produces the artefact, or
- be a phase that explicitly does not require the artefact, or
- be paused pending operator decision.

## Artefact SHA checklist

For every artefact in the handoff:

- [ ] Recorded SHA256 matches recomputed SHA256 (when verified
      locally).
- [ ] Sidecar SHA matches recomputed sidecar SHA.
- [ ] No artefact has been modified since the last merge-closeout
      (unless a phase since then explicitly modified it).

## Retained verdict / project-lock checklist

- [ ] Every retained verdict in the handoff appears verbatim in the
      latest merge-closeout.
- [ ] Every project lock in the handoff appears verbatim in the
      latest merge-closeout.
- [ ] No verdict has been silently revised.
- [ ] No project lock has been silently loosened.

If any mismatch is detected, the new chat must surface it as a
blocker and pause.

## Current arc summary

The handoff includes a one-paragraph summary of the current arc.
Example:

> The project is at the post-Phase-4bj-D merge-closeout boundary in
> the V2 microstructure → aggTrades acquisition → eligibility gate →
> normalization → derived gate → derived successor-state → feature
> kernel → feature QA → feature gate → feature research-use → feature
> successor-state → label boundary → label schema → label
> implementation → label structural QA arc. The label family is at
> Stage-0: `research_eligible = false`, `eligibility_gate_status =
> "pending"`, `chronological_split_policy = "not_yet_defined"`. The
> default next move is to remain paused. The cleanest non-paused
> conditional next phase is Phase 4bj-E — Label-Family Eligibility
> Gate Design + Implementation + Execution, which is NOT authorized.

Customize for the specific arc.

## Recommended next action

State explicitly:

- **Remain paused** (default), or
- **Author Phase {Y}** with precise scope, predecessor, allowed
  surface, and rationale.

## "Do not rely on handoff alone" rule

State explicitly in every handoff:

> This handoff is a starting point, not a substitute for current
> repo state. Before recommending or executing any phase, the new
> chat must query the repo:
>
> - read `docs/00-meta/current-project-state.md`,
> - read the most recent merge-closeout,
> - read the most recent phase implementation report,
> - confirm `git rev-parse main == git rev-parse origin/main`,
> - confirm whether the latest phase is branch-complete or
>   merge-closeout recorded,
> - confirm any local data assumptions,
> - confirm retained verdicts and project locks have not silently
>   shifted.
>
> A new chat that recommends a phase based on this handoff alone is
> unsafe.

## Template

A skeleton chat-branching handoff in markdown:

````text
# Chat Branching Handoff — Prometheus

## 1. Project identity
- **Project:** Prometheus — safety-first, rules-based,
  operator-supervised trading system for Binance USDⓈ-M futures.
- **Current arc:** {one-sentence arc identifier}.

## 2. Repository and local path
- **Repo:** Prometheus (jpedrocY/Prometheus on GitHub).
- **Local path:** `C:\Prometheus`.
- **Branch policy:** `main` is authoritative; working branches use
  `phase-{X}/{slug}` form.

## 3. Current `main` / `origin/main` SHA
- **`main`:** `{short SHA}` (`{full SHA}`).
- **`origin/main`:** `{short SHA}` (`{full SHA}`).
- **In sync:** {yes / no}.

## 4. Last completed phase
- **Phase:** {phase identifier} — {phase name}.
- **Type:** {phase type}.
- **Lifecycle state:** {"merge-closeout recorded" / "branch-complete only"}.

## 5. Last merge-closeout path
- `docs/00-meta/implementation-reports/{file}.md`

## 6. Current local data assumptions
{enumerated list of local artefacts with paths and SHA256s; or
"no local artefact assumptions"}.

## 7. Current artefacts and SHAs
{table or enumerated list of relevant artefacts with SHA256s}.

## 8. Current arc summary
{one-paragraph summary}.

## 9. Phases completed in current arc
{enumerated list of merge-closeout-recorded phases with merge-closeout
paths}.

## 10. Retained verdicts
- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 11. Project locks
- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy

All preserved verbatim.

## 12. Current non-authorizations
- ML training remains unauthorized.
- Strategy implementation remains unauthorized.
- Backtest execution remains unauthorized.
- Data acquisition remains unauthorized.
- Paper / shadow remains unauthorized.
- Live-readiness remains unauthorized.
- Deployment remains unauthorized.
- Exchange-write remains unauthorized.
- Production keys remain unauthorized.
- Authenticated APIs remain unauthorized.
- Private endpoints remain unauthorized.
- User stream remains unauthorized.
- MCP / Graphify / .mcp.json / credentials remain unauthorized.
- Manifest transition (`research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`) remains unauthorized.
- All successor phases (Phase {Y}, Phase {Z}, ...) remain
  unauthorized.

## 13. Known validation caveats
- {pre-existing failures, unchanged-from-prior-phases status; e.g.
  `KeyError: 'trade_count'` simulation failures in
  `tests/simulation/test_backtest_real_2026_03.py`}.

## 14. Recommended next phase or paused state
**Remain paused.**

{Conditional next, NOT authorized: Phase {Y} would {scope}; this is
not authorized.}

## 15. Ready-to-paste continuation prompt

```text
You are continuing work on the Prometheus project at `C:\Prometheus`.

Before recommending or executing any phase, you must:

1. Read `docs/00-meta/current-project-state.md` and identify the
   current "Current phase" block.
2. Read the most recent merge-closeout at
   `docs/00-meta/implementation-reports/{file}.md`.
3. Read the most recent phase implementation report.
4. Confirm `git rev-parse main == git rev-parse origin/main`.
5. Confirm whether the latest phase is branch-complete or
   merge-closeout recorded.
6. Confirm any local data assumptions.
7. Confirm retained verdicts and project locks have not silently
   shifted.

Do not rely on this handoff alone. Do not recommend or authorize any
phase before completing the repo-query step.

Current state at handoff time:
- `main` SHA: `{short SHA}`
- Last completed phase: {phase identifier} — {phase name}
- Last merge-closeout: `docs/00-meta/implementation-reports/{file}.md`
- Recommended next: Remain paused.
- All successor phases remain unauthorized.
- All retained verdicts preserved verbatim.
- All project locks preserved verbatim.
- All forbidden activities remain forbidden: ML, strategy,
  backtests, acquisition, paper / shadow / live, deployment,
  exchange-write, production keys, authenticated APIs, private
  endpoints, user stream, MCP, Graphify, `.mcp.json`, credentials,
  manifest transition.

When you are ready, recommend either:
- "Remain paused", or
- "Author Phase {Y}" with precise scope, predecessor, allowed
  surface, and rationale.
```
````

This standard preserves all retained verdicts and project locks
verbatim. It does not authorize any successor phase. It does not
authorize Phase 4bj-E, label-family eligibility gate implementation,
ML, strategy, backtests, acquisition, paper / shadow / live,
deployment, exchange-write, production keys, authenticated APIs,
private endpoints, user stream, MCP, Graphify, `.mcp.json`, or
credentials.
