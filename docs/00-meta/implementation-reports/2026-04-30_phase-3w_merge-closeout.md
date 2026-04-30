# Phase 3w Merge Closeout

## Summary

Phase 3w — the **docs-only remaining ambiguity-log resolution memo** — has been merged to `main` and pushed to `origin/main`. The merge resolves the three remaining OPEN ambiguity-log items (GAP-20260424-030 break-even rule conflict; GAP-20260424-031 EMA slope wording ambiguity; GAP-20260424-033 stagnation window) at the governance level using the same Phase 3v §8 pattern.

**All four Phase 3u §8.5 currently-OPEN pre-coding blockers are now RESOLVED at the governance level** (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w). Combined with the Phase 3v `stop_trigger_domain` scheme, the project record now has four binding governance label schemes for any future evidence or runtime artefact.

**No retained-evidence verdict revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim. **No policy locks changed.** §11.6 = 8 bps HIGH per side preserved. §1.7.3 mark-price-stops preserved. **No strategy rescue authorized. No Phase 4 / 4a authorized.** **No spec / backtest-plan / validation-checklist / stop-loss-policy / runtime-doc substantive edit.** Existing artefacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs) are NOT retroactively modified; the four label schemes apply prospectively.

**No code, tests, scripts, data, manifests modified beyond the ambiguity-log GAP-20260424-030 / 031 / 033 RESOLVED updates. No diagnostics rerun. No Q1–Q7 rerun. No backtests. No H-D3 / H-C2 / H-D5 sensitivity analysis. No data acquisition / patching / regeneration / modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets requested or stored.** Recommended state remains **paused**. **No successor phase has been authorized.**

## Files changed

The Phase 3w merge into `main` brought in two new files plus one targeted edit to the ambiguity log:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3w_remaining-ambiguity-log-resolution.md` — Phase 3w governance memo (552 lines; 18 sections covering Summary; Authority and boundary; Starting state; Ambiguities being resolved; Resolution principles; GAP-20260424-030 resolution (§6); GAP-20260424-031 resolution (§7); GAP-20260424-033 resolution (§8); Required future artifact labels or disclosures; Implications for retained verdicts; Implications for future backtests; Implications for future Phase 4a / runtime work; Ambiguity-log update; What this does not authorize; Forbidden-work confirmation; Remaining boundary; Operator decision menu; Next authorization status).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3w_closeout.md` — Phase 3w closeout artefact (215 lines).
- `docs/00-meta/implementation-ambiguity-log.md` — three targeted edits to GAP-20260424-030 / 031 / 033 entries only. For each entry: `Status` changed from `OPEN` to `RESOLVED — Phase 3w governance memo (2026-04-30)`. `Operator decision` records the full Phase 3w governance resolution with canonical historical provenance per-candidate and the future-runtime label-scheme guardrail. `Resolution evidence` points to the Phase 3w memo. `Related docs` extended to include Phase 3w memo, Phase 3v memo (precedent pattern), and Phase 3u §8.5 (pre-coding-blocker review). **No other ambiguity-log entry modified.**

Total Phase 3w merge: 3 file changes, 785 insertions (net of the 18 lines replaced in the three entries).

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3w_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 3w merged, GAP-20260424-030 / 031 / 033 resolved, all four Phase 3u §8.5 pre-coding blockers now resolved at governance level, four governance label schemes binding prospectively (`stop_trigger_domain`, `break_even_rule`, `ema_slope_method`, `stagnation_window_role`), `mixed_or_unknown` invalid and fails closed for all four schemes, Phase 4 remains unauthorized, Phase 4a remains conditional only and not authorized, recommended state paused, no next phase authorized, all prior verdicts and locks preserved. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 3w merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m). Mark-price 5m `research_eligible: false` preserved.
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions.
- All `src/prometheus/**` source code.
- All `scripts/**`.
- All `tests/**`.
- All `.claude/rules/**`.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v reports / closeouts / merge-closeouts.
- `docs/03-strategy-research/v1-breakout-strategy-spec.md` — substantive content preserved verbatim. Lines 156–172, 380, 415, 564 unchanged.
- `docs/03-strategy-research/v1-breakout-backtest-plan.md` — preserved verbatim.
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` — preserved verbatim.
- `docs/07-risk/stop-loss-policy.md` — preserved verbatim.
- `docs/06-execution-exchange/binance-usdm-order-model.md` — preserved verbatim.
- `docs/12-roadmap/phase-gates.md` — preserved verbatim.
- `docs/12-roadmap/technical-debt-register.md` — preserved verbatim.

## Phase 3w commits included

| Commit | Subject |
|---|---|
| `29054ce8a0cc43854283e96c802e549531e0ae7d` | `phase-3w: remaining ambiguity-log resolution memo (docs-only)` — Phase 3w governance memo + ambiguity-log GAP-20260424-030 / 031 / 033 RESOLVED updates. |
| `85f52dc6dc71437cd8708f9b7c411816e31301be` | `docs(phase-3w): closeout report (Markdown artefact)` — Phase 3w closeout. |

## Merge commit

- **Phase 3w merge commit (`--no-ff`, ort strategy):** `df161da1557c1f6eeaa6b5a9571ddb8a75d4b10f`
- **Merge title:** `Merge Phase 3w (docs-only remaining ambiguity-log resolution memo: GAP-20260424-030 / 031 / 033) into main`

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 3w merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `df161da` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern, the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-3w): merge closeout + current-project-state sync
df161da  Merge Phase 3w (docs-only remaining ambiguity-log resolution memo: GAP-20260424-030 / 031 / 033) into main
85f52dc  docs(phase-3w): closeout report (Markdown artefact)
29054ce  phase-3w: remaining ambiguity-log resolution memo (docs-only)
fdbbfab  docs(phase-3v): merge closeout + current-project-state sync
15ba71c  Merge Phase 3v (docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo) into main
5be9978  docs(phase-3v): closeout report (Markdown artefact)
671f6e2  phase-3v: GAP-20260424-032 stop-trigger domain ambiguity resolution memo (docs-only)
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-3w/remaining-ambiguity-log-resolution`**: `85f52dc6dc71437cd8708f9b7c411816e31301be` (branch tip preserved).
- **`git rev-parse origin/phase-3w/remaining-ambiguity-log-resolution`**: `85f52dc6dc71437cd8708f9b7c411816e31301be`.
- **`git rev-parse phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7` (branch tip preserved).
- **`git rev-parse phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (branch tip preserved).
- **`git rev-parse phase-3t/post-5m-diagnostics-consolidation`**: `fcf8192e150e7dc783da345d2e54be8cff1611db` (branch tip preserved).
- **`git rev-parse phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a` (branch tip preserved).
- **`git rev-parse phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (branch tip preserved).
- **`git rev-parse phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (branch tip preserved).

## main == origin/main confirmation

After the Phase 3w merge push: local `main` = `origin/main` = `df161da1557c1f6eeaa6b5a9571ddb8a75d4b10f`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## GAP resolution summary

- **GAP-20260424-030** — Break-even rule text conflicts with spec Open Question #8. **RESOLVED — Phase 3w governance memo (2026-04-30).** Historical break-even-rule provenance per Phase 3w §6.1: H0 / R1a / R1b-narrow / R2 = `break_even_rule = enabled_plus_1_5R_mfe` (Stage-4 staged-trailing per spec line 380); R3 / F1 / D1-A = `break_even_rule = disabled` (R3 replaced staged-trailing with Fixed-R + 8-bar time-stop; F1 / D1-A independent exit families). Future-runtime guardrail per Phase 3w §6.3: `break_even_rule` label scheme.
- **GAP-20260424-031** — EMA slope wording ambiguous: discrete comparison vs. fitted slope. **RESOLVED — Phase 3w governance memo (2026-04-30).** Historical EMA-slope provenance per Phase 3w §7.1: V1-family backtests (H0 / R1a / R1b-narrow / R2 / R3) = `ema_slope_method = discrete_comparison` (`EMA[now] > EMA[now − 3h]`); F1 / D1-A = `ema_slope_method = not_applicable` (no 1h EMA bias primary entry filter). Future-runtime guardrail per Phase 3w §7.3: `ema_slope_method` label scheme. H-C2 fitted-slope variant remains separately-predeclared future hypothesis (not authorized).
- **GAP-20260424-033** — Stagnation window not in Open Questions but discussed as metric. **RESOLVED — Phase 3w governance memo (2026-04-30).** Historical stagnation-window provenance per Phase 3w §8.1: H0 / R1a / R1b-narrow / R2 = `stagnation_window_role = active_rule_predeclared` (`stagnation_bars = 8`, `stagnation_min_mfe_R = +1.0 R` per spec line 415); R3 / F1 / D1-A = `stagnation_window_role = not_active` (replaced by unconditional time-stops). Future-runtime guardrail per Phase 3w §8.3: `stagnation_window_role` label scheme. H-D5 stagnation-window variant remains separately-predeclared future hypothesis (not authorized).
- **GAP-20260424-032** — Backtest uses trade-price stops; live uses MARK_PRICE stops. **Remains RESOLVED from Phase 3v governance memo (2026-04-30).** Stop-trigger-domain governance per Phase 3v §8.4: `stop_trigger_domain` label scheme; future runtime / paper / live remains MARK_PRICE-locked.
- **All four Phase 3u §8.5 pre-coding blockers are now resolved at governance level.**
- **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. All preserved verbatim.
- **No strategy rescue was authorized.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, 5m-on-X variant, or any other successor authorized.
- **No Phase 4 or Phase 4a was authorized.** Phase 3u §16 + Phase 3v §17 + Phase 3w §17 recommendations stand; Phase 4 (canonical) remains unauthorized; Phase 4a (safe slice) remains conditional only and not authorized.

## Governance label summary

The following four governance label schemes are now binding from the Phase 3w merge forward on any future evidence or runtime artefact:

| Label | Source | Valid values | Fail-closed |
|---|---|---|---|
| `stop_trigger_domain` | Phase 3v §8.4 | `trade_price_backtest`, `mark_price_runtime`, `mark_price_backtest_candidate` | `mixed_or_unknown` |
| `break_even_rule` | Phase 3w §6.3 | `disabled`, `enabled_plus_1_5R_mfe`, `enabled_plus_2_0R_mfe`, `enabled_<other_predeclared>` | `mixed_or_unknown` |
| `ema_slope_method` | Phase 3w §7.3 | `discrete_comparison`, `fitted_slope`, `other_predeclared`, `not_applicable` | `mixed_or_unknown` |
| `stagnation_window_role` | Phase 3w §8.3 | `not_active`, `metric_only`, `active_rule_predeclared` | `mixed_or_unknown` |

For all four schemes, **`mixed_or_unknown` is invalid and fails closed at any decision boundary** (block trade / block verdict / block persist / block evidence-promotion).

Future runtime / backtest / dashboard / persistence / event-contract artefacts must declare these labels as first-class fields. Existing artefacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs) are NOT retroactively modified; they should be treated as having the implicit labels recorded in the Phase 3w / Phase 3v memos for audit purposes.

## Remaining blockers

After Phase 3w, `docs/00-meta/implementation-ambiguity-log.md` has **zero OPEN entries that constitute pre-coding blockers** per Phase 3u §8.5.

Pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED`) remain as documented in the ambiguity log and `docs/12-roadmap/technical-debt-register.md`. These are **not pre-coding blockers**; they are pre-tiny-live concerns reviewed before any future tiny-live transition. Notable items:

- GAP-20260419-018 — Taker commission rate parameterization (`ACCEPTED_LIMITATION`).
- GAP-20260419-020 — ExchangeInfo snapshot proxy (`ACCEPTED_LIMITATION`).
- GAP-20260419-024 — leverageBracket placeholder (`ACCEPTED_LIMITATION`).
- GAP-20260419-025 — Wider historical backfill (`DEFERRED`).
- TD-006 (`docs/12-roadmap/technical-debt-register.md`) — Exact Binance endpoint behavior verification (partially resolved at coding time for bulk klines + mark-price; remains open for REST-write paths and user-stream behavior).
- TD-017 — Public-IP solution for local NUC (pre-tiny-live).
- TD-018 — First live notional cap value (pre-tiny-live).
- TD-019 — Production alert route selection (pre-tiny-live).
- TD-020 — Backup schedule and retention (pre-tiny-live).

These pre-tiny-live items are documented for completeness; they would be addressed by a separately authorized pre-tiny-live readiness phase if and when paper/shadow / Phase 4 / live-readiness work is ever authorized. **Phase 3w does not authorize any such phase.**

## Forbidden-work confirmation

- **No Phase 3x / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No Phase 4 / Phase 4a started.** Phase 3w recommends Phase 4 remain unauthorized and Phase 4a remain conditional only; the merge does not change those recommendations into authorizations.
- **No implementation code written.** Phase 3w is text-only (memo + ambiguity-log entry edits); the merge brings in pre-existing Phase 3w artefacts unchanged.
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun. No new diagnostic computation.
- **No Q1–Q7 rerun.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No H-D3 / H-C2 / H-D5 sensitivity analysis.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. **§11.6 unchanged.** **§1.7.3 unchanged.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.** Spec lines 156–172, 380, 415, 564 all preserved verbatim.
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No strategy rescue proposal.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, or 5m-on-X variant.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription.**
- **No public endpoints consulted.** This merge + housekeeping commit performs no network I/O.
- **No secrets requested or stored.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `df161da`. Phase 3w memo + ambiguity-log updates + closeout consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8.
- **Break-even rule governance:** RESOLVED by Phase 3w §6.
- **EMA slope method governance:** RESOLVED by Phase 3w §7.
- **Stagnation window role governance:** RESOLVED by Phase 3w §8.
- **OPEN ambiguity-log items after Phase 3w:** zero relevant to Phase 4a / runtime / strategy implementation. All four Phase 3u §8.5 currently-OPEN pre-coding blockers RESOLVED at the governance level.
- **Pre-tiny-live items:** documented but not pre-coding blockers; would be addressed by a separately authorized pre-tiny-live readiness phase if/when paper/shadow / Phase 4 / live-readiness work is ever authorized.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-3w/remaining-ambiguity-log-resolution` pushed at `85f52dc`. Commits in main via Phase 3w merge.
  - All prior phase branches preserved at their respective tips.

## Next authorization status

**No next phase has been authorized.** Phase 3w recommended Option A (remain paused) as primary; Option B (Phase 4a safe-slice scoping memo per Phase 3u §16.3 + Phase 3v §17.3) as conditional secondary subject to Phase 3u §10 anti-live-readiness preconditions; Option C (sensitivity analyses on retained-evidence populations: H-D3 / H-C2 / H-D5 / mark-price-stop) as conditional alternative not recommended now (low expected new information; high procedural cost); Options D (fresh-hypothesis research) and E (Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write) NOT recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
