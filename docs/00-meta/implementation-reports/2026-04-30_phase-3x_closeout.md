# Phase 3x Closeout

## Summary

Phase 3x — the **docs-only Phase 4a safe-slice scoping memo** — is committed on branch `phase-3x/phase-4a-safe-slice-scoping` and pushed to `origin/phase-3x/phase-4a-safe-slice-scoping`. The memo defines what a possible future Phase 4a execution phase would be (a strictly local-only, fake-exchange, dry-run, exchange-write-free implementation scope) and what it must categorically not be. **Phase 3x does NOT authorize Phase 4a execution.** Phase 3x is a scoping memo only.

The memo (903 lines; 19 sections) covers: Summary; Authority and boundary; Starting state; Why this memo exists; What Phase 4a would be; What Phase 4a must not be; Preconditions satisfied; Preconditions still not satisfied; Safe-slice candidate scope (10 components evaluated); Explicitly out-of-scope work; Required governance labels; Fail-closed requirements; Required implementation evidence if later authorized; Required tests if later authorized; Required documentation updates if later authorized; Risks and mitigations; Recommendation; Operator decision menu; Next authorization status.

**No retained-evidence verdict revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim. **No policy locks changed.** §11.6 = 8 bps HIGH per side preserved. §1.7.3 mark-price-stops preserved. Phase 3v §8 stop-trigger-domain governance preserved. Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance preserved. **No strategy rescue authorized.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, 5m-on-X variant, or any other successor authorized. **No Phase 4 / 4a authorized.** Phase 3u §16 + Phase 3v §17 + Phase 3w §17 + Phase 3x §17 / §18 recommendations stand; Phase 4 (canonical) remains unauthorized; Phase 4a execution remains conditional only and not authorized.

**No code, tests, scripts, data, manifests modified.** No diagnostics run. No Q1–Q7 rerun. No backtests. No H-D3 / H-C2 / H-D5 sensitivity analysis. No mark-price-stop sensitivity analysis. No data acquisition / patching / regeneration / modification. No `data/manifests/*.manifest.json` modification. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No v003 created. No spec / backtest-plan / validation-checklist / stop-loss-policy / runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff / first-run-setup-checklist substantive edit. No `.claude/rules/**` modification. No `src/prometheus/**` modification. No `scripts/**` modification. No `tests/**` modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets requested or stored. **Recommended state remains paused.** **No successor phase has been authorized.**

## Files changed

- `docs/00-meta/implementation-reports/2026-04-30_phase-3x_phase-4a-safe-slice-scoping.md` — Phase 3x scoping memo (new file; 903 lines; committed as `14bfb38b`).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3x_closeout.md` — this closeout artefact (new file).

No other file modified by Phase 3x. Specifically NOT modified:

- `docs/00-meta/current-project-state.md` — preserved unchanged on the Phase 3x branch (per the brief's "Allowed changes" section: optional narrow update only after merge if appropriate; Phase 3x prefers no `current-project-state.md` update until merge).
- `docs/00-meta/implementation-ambiguity-log.md` — preserved verbatim. No new ambiguity surfaced by Phase 3x scoping; all four pre-coding blockers remain RESOLVED per Phase 3v / 3w.
- `docs/12-roadmap/phase-gates.md` — preserved verbatim.
- `docs/12-roadmap/technical-debt-register.md` — preserved verbatim. Pre-tiny-live items (TD-006 / TD-017 / TD-018 / TD-019 / TD-020) remain documented as pre-tiny-live concerns and are NOT pre-coding blockers per Phase 3u §8.2 / Phase 3w §16.
- `docs/00-meta/ai-coding-handoff.md` — preserved verbatim.
- `docs/09-operations/first-run-setup-checklist.md` — preserved verbatim.
- All `docs/03-strategy-research/*` — preserved verbatim. Strategy spec lines 156–172, 332, 380, 415, 564 unchanged.
- All `docs/04-data/*` — preserved verbatim.
- All `docs/05-backtesting-validation/*` — preserved verbatim.
- All `docs/06-execution-exchange/*` — preserved verbatim.
- All `docs/07-risk/*` — preserved verbatim.
- All `docs/08-architecture/*` — preserved verbatim.
- All `docs/09-operations/*` (other than this closeout — wait, this closeout is in `docs/00-meta/implementation-reports/`, not `docs/09-operations/`). All `docs/09-operations/*` preserved verbatim.
- All `docs/10-security/*` — preserved verbatim.
- All `docs/11-interface/*` — preserved verbatim.
- All `data/manifests/*.manifest.json` — preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions (git-ignored per repo convention).
- All `src/prometheus/**` — preserved verbatim.
- All `scripts/**` — preserved verbatim.
- All `tests/**` — preserved verbatim.
- All `.claude/rules/**` — preserved verbatim.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w reports / closeouts / merge-closeouts — preserved verbatim.
- `.mcp.json` — preserved (no changes; no new MCP servers enabled).
- `pyproject.toml` — preserved verbatim.
- `.gitignore` — preserved verbatim.

## Safe-slice scoping conclusion

Phase 3x scoping memo concludes:

1. **All four Phase 3u §8.5 currently-OPEN pre-coding governance blockers are RESOLVED at the governance level.** GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w. The procedural ground for *any* coding work is therefore cleaner than at Phase 3u. This does NOT itself authorize coding; it only removes the governance-level blockers Phase 3u flagged.

2. **A future Phase 4a execution phase, if ever authorized, must be a strict subset of canonical Phase 4** with explicit anti-live-readiness preconditions. The §6 prohibition list is binding: no live exchange-write capability; no production Binance keys; no authenticated APIs / private endpoints / user stream / WebSocket; no paper/shadow; no live-readiness implication; no deployment; no strategy commitment / rescue / new candidate; no verdict revision; no lock change; no MCP / Graphify / `.mcp.json` / credentials; no data acquisition / patching / regeneration / modification; no regime-first / ML / cost-model-revision work.

3. **Ten candidate Phase 4a components are scoped and assessed as appropriate for the strict-subset framing.** Runtime mode / state model; runtime control state persistence; internal event contracts; risk sizing skeleton; exposure gate skeleton; stop-validation skeleton; break-even / EMA / stagnation governance label plumbing; fake-exchange adapter; read-only operator state view; test harness. Each is local-only, fake-exchange or fake-state-only, dry-run, exchange-write-free, strategy-agnostic, and lock-preserving.

4. **The four governance label schemes (Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3) become enforceable in code at the Phase 4a layer** if Phase 4a is ever authorized. `stop_trigger_domain` | `break_even_rule` | `ema_slope_method` | `stagnation_window_role`. `mixed_or_unknown` must fail closed at any decision boundary.

5. **Phase 3x is a scoping memo only.** Phase 3x does NOT authorize Phase 4a execution. Authorizing Phase 4a execution would require a separate operator decision after Phase 3x is reviewed, with the operator's authorization brief reaffirming the §6 prohibition list verbatim and committing to the §18.2 preconditions (especially the §16.6 conscious-research-deprioritization commitment, or an explicit waiver with written rationale).

## Candidate future Phase 4a scope

If the operator ever authorizes Phase 4a execution, the candidate scope (per Phase 3x §9) consists of ten components:

1. **Runtime mode / state model** — In-process state machine (`SAFE_MODE`, `RUNNING`, `BLOCKED`, `EMERGENCY`, `RECOVERY_REQUIRED`); unknown state must fail closed.
2. **Runtime control state persistence** — SQLite / local persistence only; startup defaults to `SAFE_MODE`; kill-switch state persists across restart; no automatic kill-switch clearing.
3. **Internal event contracts** — Typed local events only; no exchange-write events; no authenticated-exchange events; event schema must carry required governance labels where relevant.
4. **Risk sizing skeleton** — Local calculation only; no order placement; fail closed on missing metadata; respect 0.25% risk and 2× leverage cap as locked constants if referenced; no live notional decision.
5. **Exposure gate skeleton** — One-symbol-only live lock preserved; one-position max preserved; no pyramiding / no reversal guardrails; fake-position state only.
6. **Stop-validation skeleton** — Must enforce Phase 3v `stop_trigger_domain` labels; `mark_price_runtime` required for any future runtime / live path; `mixed_or_unknown` fails closed; no order placement; no stop widening.
7. **Break-even / EMA / stagnation governance label plumbing** — `break_even_rule`, `ema_slope_method`, `stagnation_window_role` labels; `mixed_or_unknown` fails closed; label persistence / observability only, not strategy changes.
8. **Fake-exchange adapter** — Local deterministic fake adapter only; no Binance credentials; no private endpoints; no WebSocket; no real order placement; no real cancellation; no account state mutation.
9. **Read-only operator state view** — Local dashboard / read model acceptable only if read-only; no control buttons that imply live execution; no exchange actions; no production alerting.
10. **Test harness** — Unit tests for fail-closed behavior; restart safety tests; kill-switch persistence tests; label validation tests; fake-exchange lifecycle tests; no live integration tests.

A future Phase 4a execution brief would explicitly authorize one or more of these components (or all of them, or a stricter subset). Phase 3x does NOT authorize any of them.

## Explicitly forbidden work

The following work is categorically forbidden in any future Phase 4a execution (per Phase 3x §6 + §10):

- **No live exchange-write capability** — categorically. Architectural prohibition: live exchange adapter is not implemented; only fake adapter exists in code.
- **No production Binance keys** — never requested, stored, configured, or used.
- **No authenticated APIs / private endpoints / user stream / WebSocket** — code paths simply do not contain these.
- **No paper/shadow** — Phase 4a is not Phase 7 territory.
- **No live-readiness implication** — every Phase 4a-related artefact must include a "no live-readiness, no exchange-write, no strategy commitment" disclaimer.
- **No deployment** — no deployment artefact for live operation; no NUC live setup; no Telegram / n8n production alerting.
- **No strategy commitment / rescue / new candidate** — Phase 4a is strategy-agnostic; the runtime accepts any future authorized strategy without privileging one.
- **No verdict revision** — R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No lock change** — §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim.
- **No MCP / Graphify / `.mcp.json` / credentials** — none enabled, configured, requested, or stored.
- **No data acquisition / patching / regeneration / modification** — `data/` artefacts preserved verbatim.
- **No regime-first / ML / cost-model-revision work** — preserved as not-recommended-now per prior phase recommendations.
- **No retroactive modification of Phase 2 / Phase 3 backtest manifests, Phase 3q v001-of-5m manifests, or Phase 3s diagnostic outputs** — the four governance label schemes apply prospectively only.

## Recommendation

**Phase 3x recommends Option A (remain paused) as primary**, with explicit acknowledgment that Option B (authorize future Phase 4a execution as local-only safe-slice) is now procedurally well-grounded given that all four Phase 3u §8.5 pre-coding governance blockers are RESOLVED at the governance level (per Phase 3v / Phase 3w).

Operator decision menu:

- **Option A — Remain paused (PRIMARY).** Take no further action. The strategic pause continues. Phase 3x's scoping value is realized by the memo itself; future runtime / paper / live work, if ever authorized, would inherit the §6 prohibition list and the four governance label schemes regardless.
- **Option B — Authorize future Phase 4a execution as local-only safe-slice (CONDITIONAL secondary; now procedurally well-grounded).** Subject to the §18.2 preconditions: operator commits ex-ante to §6 prohibition list verbatim; operator commits ex-ante to §10 out-of-scope list; operator commits ex-ante that authorizing execution does not commit the project to live readiness; operator commits ex-ante that Phase 4a success does not authorize paper/shadow / tiny live / any subsequent phase; operator selects §9 component scope and explicitly authorizes that scope; operator commits ex-ante that the four governance label schemes will be enforced in code at every decision boundary; operator commits ex-ante that pre-tiny-live items remain pre-tiny-live concerns; operator commits ex-ante (preferably) to a defined research-deprioritization period or alternatively explicitly waives §16.6 with written rationale.
- **Option C — More docs-only preparation first (CONDITIONAL tertiary).** Authorize one or more additional docs-only memos before any Phase 4a execution: a Phase 4a execution-plan memo with per-commit acceptance criteria; a label-enforcement design memo specifying code-level form of the four governance label schemes; a documentation-refresh memo updating implementation-blueprint / ai-coding-handoff / phase-gates with explicit Phase 4a sub-scope language.
- **Option D — Return to research / sensitivity analysis (NOT RECOMMENDED).** Per Phase 3v §17.4 + Phase 3w §17.3 + Phase 3w §17.4. Bounded marginal information value. Procedurally heavy.
- **Option E — Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write (FORBIDDEN / NOT RECOMMENDED).** Per `phase-gates.md`, none of these gates is met.

## Commit

| Commit | Subject |
|---|---|
| `14bfb38bab358224402b86831f89b787560157db` | `phase-3x: Phase 4a safe-slice scoping memo (docs-only)` — Phase 3x scoping memo. |
| _(this commit)_ | `docs(phase-3x): closeout report (Markdown artefact)` — Phase 3x closeout. |

Both commits are on branch `phase-3x/phase-4a-safe-slice-scoping`. Branch pushed to `origin/phase-3x/phase-4a-safe-slice-scoping`. Per prior phase pattern, this closeout file's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged. The closeout commit's SHA is reported in the chat closeout block accompanying this commit.

## Final git status

```text
clean
```

Working tree empty after both commits on the Phase 3x branch. No uncommitted changes. No untracked files.

## Final git log --oneline -5

Snapshot at the closeout commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this closeout commit itself is committed>  docs(phase-3x): closeout report (Markdown artefact)
14bfb38  phase-3x: Phase 4a safe-slice scoping memo (docs-only)
75e5029  docs(phase-3w): merge closeout + current-project-state sync
df161da  Merge Phase 3w (docs-only remaining ambiguity-log resolution memo: GAP-20260424-030 / 031 / 033) into main
85f52dc  docs(phase-3w): closeout report (Markdown artefact)
```

## Final rev-parse

- **`git rev-parse HEAD`** (on `phase-3x/phase-4a-safe-slice-scoping`): the closeout commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse phase-3x/phase-4a-safe-slice-scoping`**: same as `HEAD` above.
- **`git rev-parse origin/phase-3x/phase-4a-safe-slice-scoping`**: same as `HEAD` above (after push).
- **`git rev-parse main`**: `75e5029b11620d9540106137c7449b20df1aedc1` (unchanged from pre-Phase-3x).
- **`git rev-parse origin/main`**: `75e5029b11620d9540106137c7449b20df1aedc1` (unchanged).
- **`git rev-parse phase-3w/remaining-ambiguity-log-resolution`**: `85f52dc6dc71437cd8708f9b7c411816e31301be` (preserved).
- **`git rev-parse phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7` (preserved).
- **`git rev-parse phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (preserved).

## Branch / main status

- **`phase-3x/phase-4a-safe-slice-scoping`** — pushed to `origin/phase-3x/phase-4a-safe-slice-scoping`. Two commits on the branch: the Phase 3x scoping memo (`14bfb38b`) and this closeout (SHA reported in chat closeout). Branch NOT merged to `main`.
- **`main`** — unchanged at `75e5029b11620d9540106137c7449b20df1aedc1`. Local `main` = `origin/main` = `75e5029b`.
- **No merge to main.** Per the Phase 3x brief: "Do not merge to main unless explicitly instructed."

## Forbidden-work confirmation

- **No Phase 4 / Phase 4a execution started.** Phase 3x is a scoping memo only. The memo defines what Phase 4a execution would entail if ever authorized; it does not authorize execution.
- **No implementation code written.** Phase 3x is text-only.
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No diagnostics run.** No Q1–Q7 rerun. No new diagnostic computation.
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No H-D3 / H-C2 / H-D5 sensitivity analysis. No mark-price-stop sensitivity analysis on retained-evidence populations.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified. No public Binance endpoint consulted. No private endpoint consulted. Phase 3x performs no network I/O.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. **§11.6 unchanged.** **§1.7.3 mark-price-stop lock unchanged.**
- **No Phase 3v stop-trigger-domain governance modification.** Phase 3v §8.4 label scheme preserved verbatim.
- **No Phase 3w break-even / EMA slope / stagnation governance modification.** Phase 3w §6.3 / §7.3 / §8.3 label schemes preserved verbatim.
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.** Spec lines 156–172, 332, 380, 415, 564 all preserved verbatim.
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.** All four pre-coding blockers (GAP-20260424-030 / 031 / 032 / 033) remain RESOLVED per Phase 3v / Phase 3w. No new entry added by Phase 3x; no existing entry modified by Phase 3x.
- **No `docs/00-meta/current-project-state.md` modification on the Phase 3x branch.** Per the Phase 3x brief's "Allowed changes" section, the `current-project-state.md` update is preferred only after merge.
- **No strategy rescue proposal.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, or 5m-on-X variant.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription.**
- **No public endpoints consulted.** Phase 3x performs no network I/O.
- **No secrets requested or stored.**
- **No `.claude/rules/**` modification.**
- **No `src/prometheus/**` modification.**
- **No `scripts/**` modification.**
- **No `tests/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a execution remains conditional only and not authorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8.
- **Break-even rule governance:** RESOLVED by Phase 3w §6.
- **EMA slope method governance:** RESOLVED by Phase 3w §7.
- **Stagnation window role governance:** RESOLVED by Phase 3w §8.
- **Phase 4a safe-slice scope:** Defined by Phase 3x — this memo. The §6 prohibition list is binding on any future Phase 4a execution authorization brief. The four governance label schemes (Phase 3v + Phase 3w) become enforceable in code at the Phase 4a layer if Phase 4a is ever authorized.
- **OPEN ambiguity-log items after Phase 3x:** zero relevant to Phase 4a / runtime / strategy implementation. Pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED`) remain documented as pre-tiny-live concerns and are NOT pre-coding blockers.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-3x/phase-4a-safe-slice-scoping` pushed to `origin/phase-3x/phase-4a-safe-slice-scoping`. Two commits on the branch (memo + closeout). NOT merged to main.
  - All prior phase branches preserved at their respective tips.

## Next authorization status

**No next phase has been authorized.** Phase 3x recommended Option A (remain paused) as primary; Option B (authorize future Phase 4a execution as local-only safe-slice) as conditional secondary now procedurally well-grounded subject to §18.2 preconditions; Option C (more docs-only preparation: Phase 4a execution-plan memo, label-enforcement design memo, or documentation-refresh memo) as conditional tertiary; Option D (return to research / sensitivity analysis: H-D3 / H-C2 / H-D5 / mark-price-stop sensitivity / fresh-hypothesis research) NOT recommended; Option E (Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write) FORBIDDEN / NOT RECOMMENDED.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
