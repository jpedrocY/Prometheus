# Phase 3w Closeout

## Summary

Phase 3w (docs-only) formally resolved the **three remaining OPEN ambiguity-log items** (GAP-20260424-030 break-even rule conflict; GAP-20260424-031 EMA slope wording ambiguity; GAP-20260424-033 stagnation window) at the governance level using the same Phase 3v §8 pattern (historical provenance preserved; future runtime / paper / live forced to label semantic choice explicitly; `mixed_or_unknown` fails closed; no retained verdict revised; no strategy parameter / threshold / lock changed; no Phase 4 / 4a authorization).

**After Phase 3w, all four Phase 3u §8.5 currently-OPEN pre-coding blockers are RESOLVED at the governance level** (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w). The four label schemes are binding from the Phase 3w commit forward on any future evidence or runtime artefact:

| Label | Valid values | Fail-closed |
|---|---|---|
| `stop_trigger_domain` (Phase 3v §8.4) | `trade_price_backtest` \| `mark_price_runtime` \| `mark_price_backtest_candidate` | `mixed_or_unknown` |
| `break_even_rule` (Phase 3w §6.3) | `disabled` \| `enabled_plus_1_5R_mfe` \| `enabled_plus_2_0R_mfe` \| `enabled_<other_predeclared>` | `mixed_or_unknown` |
| `ema_slope_method` (Phase 3w §7.3) | `discrete_comparison` \| `fitted_slope` \| `other_predeclared` \| `not_applicable` | `mixed_or_unknown` |
| `stagnation_window_role` (Phase 3w §8.3) | `not_active` \| `metric_only` \| `active_rule_predeclared` | `mixed_or_unknown` |

**No retained-evidence verdict revised. No policy locks changed. No strategy rescue authorized. No Phase 4 / 4a authorized.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance — all preserved verbatim. No `docs/03-strategy-research/v1-breakout-strategy-spec.md`, `docs/03-strategy-research/v1-breakout-backtest-plan.md`, or `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive edit (Phase 3w opted not to make optional cross-reference back-pointers because the Phase 3w memo + ambiguity-log RESOLVED entries are sufficient pointers).

**Phase 3w is not merged. No successor phase has been authorized.** Recommendation: **remain paused (primary).**

## Files changed

Phase 3w memo branch (`phase-3w/remaining-ambiguity-log-resolution`) committed two file changes; one new file under `docs/00-meta/implementation-reports/` and one targeted edit to the ambiguity log:

- **NEW:** `docs/00-meta/implementation-reports/2026-04-30_phase-3w_remaining-ambiguity-log-resolution.md` — Phase 3w governance memo (552 lines; 18 sections covering Summary; Authority and boundary; Starting state; Ambiguities being resolved; Resolution principles; GAP-20260424-030 resolution (§6); GAP-20260424-031 resolution (§7); GAP-20260424-033 resolution (§8); Required future artifact labels or disclosures; Implications for retained verdicts; Implications for future backtests; Implications for future Phase 4a / runtime work; Ambiguity-log update; What this does not authorize; Forbidden-work confirmation; Remaining boundary; Operator decision menu; Next authorization status). Committed at `29054ce`.
- **EDITED:** `docs/00-meta/implementation-ambiguity-log.md` — three targeted edits to GAP-20260424-030 / 031 / 033 entries only. For each entry: `Status` changed from `OPEN` to `RESOLVED — Phase 3w governance memo (2026-04-30)`. `Operator decision` records the full Phase 3w governance resolution with canonical historical provenance per-candidate and the future-runtime label-scheme guardrail. `Resolution evidence` points to the Phase 3w memo. `Related docs` extended to include Phase 3w memo, Phase 3v memo (precedent pattern), and Phase 3u §8.5 (pre-coding-blocker review). **No other ambiguity-log entry modified.** Committed in the same commit.

This closeout-file commit additionally adds:

- **NEW:** `docs/00-meta/implementation-reports/2026-04-30_phase-3w_closeout.md` — this file.

NOT modified by Phase 3w:

- All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m). Mark-price 5m `research_eligible: false` preserved.
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions.
- All `src/prometheus/**` source code.
- All `scripts/**`.
- All `tests/**`.
- All `.claude/rules/**`.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v reports / closeouts / merge-closeouts.
- `docs/03-strategy-research/v1-breakout-strategy-spec.md` — substantive content preserved verbatim. Phase 3w memo notes that optional cross-reference back-pointers were permitted but Phase 3w opted not to make them.
- `docs/03-strategy-research/v1-breakout-backtest-plan.md` — preserved verbatim.
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` — preserved verbatim.
- `docs/07-risk/stop-loss-policy.md` — preserved verbatim.
- `docs/06-execution-exchange/binance-usdm-order-model.md` — preserved verbatim.
- `docs/12-roadmap/phase-gates.md` — preserved verbatim.
- `docs/12-roadmap/technical-debt-register.md` — preserved verbatim.
- `docs/00-meta/current-project-state.md` — no Phase 3w line added (Phase 3w is not merged; no current-state update appropriate at branch state).
- All other `docs/**` files.

## GAP-20260424-030 resolution

**GAP-20260424-030 — Break-even rule text conflicts with spec Open Question #8.** Status: **RESOLVED — Phase 3w governance memo (2026-04-30)**.

Historical canonical provenance (Phase 3w §6.1):

| Candidate | `break_even_rule` | Reasoning |
|---|---|---|
| H0 / R1a / R1b-narrow / R2 | `enabled_plus_1_5R_mfe` | Inherits H0 staged-trailing exit; Stage-4 break-even at +1.5 R MFE per spec line 380. |
| R3 (baseline-of-record) | `disabled` | Phase 2p §C.1 replaced staged-trailing with Fixed-R + 8-bar time-stop; staged-trailing structurally absent. |
| F1 / D1-A | `disabled` | Independent exit families (mean-reversion target + 8-bar time-stop; funding-extreme target + 32-bar time-stop). |

H-D3 wave-1 variant tested `enabled_plus_2_0R_mfe`; not promoted forward.

Future runtime guardrail (Phase 3w §6.3): `break_even_rule` label scheme; `mixed_or_unknown` fails closed.

No retroactive spec edit. No retained verdict revised. No break-even rule added, removed, or changed. No future H-D3-style break-even variant phase authorized.

## GAP-20260424-031 resolution

**GAP-20260424-031 — EMA slope wording ambiguous: discrete comparison vs. fitted slope.** Status: **RESOLVED — Phase 3w governance memo (2026-04-30)**.

Historical canonical provenance (Phase 3w §7.1):

| Candidate | `ema_slope_method` | Reasoning |
|---|---|---|
| H0 / R1a / R1b-narrow / R2 / R3 | `discrete_comparison` | V1-family backtests used `EMA[now] > EMA[now − 3h]` (long) / `EMA[now] < EMA[now − 3h]` (short). Phase 2f memo confirmed this as the working implementation convention. |
| F1 / D1-A | `not_applicable` | Independent strategy families that do not use 1h EMA bias as primary entry filter. |

H-C1 wave-1 variant tested a different EMA pair (20/100) but preserved discrete-comparison interpretation. H-C2 fitted-slope variant remains separately-predeclared future hypothesis; no fitted-slope evidence exists in the retained-evidence record.

Future runtime guardrail (Phase 3w §7.3): `ema_slope_method` label scheme; `mixed_or_unknown` fails closed.

No retroactive spec edit. No retained verdict revised. No EMA logic changed. No future H-C2-style fitted-slope variant phase authorized.

## GAP-20260424-033 resolution

**GAP-20260424-033 — Stagnation window not in Open Questions but discussed as metric.** Status: **RESOLVED — Phase 3w governance memo (2026-04-30)**.

Historical canonical provenance (Phase 3w §8.1):

| Candidate | `stagnation_window_role` | Reasoning |
|---|---|---|
| H0 / R1a / R1b-narrow / R2 | `active_rule_predeclared` (`stagnation_bars = 8`, `stagnation_min_mfe_R = +1.0 R`) | Stagnation rule active per spec line 415: "if, after 8 completed 15m bars from entry, the trade has not reached at least +1.0 R MFE, exit at market." |
| R3 (baseline-of-record) | `not_active` | Phase 2p §C.1 replaced staged-trailing (which included stagnation) with Fixed-R + unconditional 8-bar time-stop. R3's 8-bar time-stop fires unconditionally regardless of MFE — structurally different from H0's stagnation rule (which fires at 8 bars only if MFE < +1.0 R). |
| F1 | `not_active` | Independent exit family (8-bar cumulative-displacement target + structural stop + 8-bar unconditional time-stop). |
| D1-A | `not_active` | Independent exit family (Fixed-R target + 32-bar unconditional time-stop). |

H-D5 wave-1+ variant (stagnation-window 6/10/12 bars) was deferred and remains its own predeclared future hypothesis; no H-D5 evidence exists in the retained-evidence record.

Future runtime guardrail (Phase 3w §8.3): `stagnation_window_role` label scheme; `mixed_or_unknown` fails closed.

No retroactive spec edit. No backtest-plan §Metrics — stagnation-exit frequency edit. No retained verdict revised. No stagnation rule, filter, exit, or metric added or removed from any candidate. No future H-D5-style stagnation-window variant phase authorized.

## Ambiguity-log update

`docs/00-meta/implementation-ambiguity-log.md` updates (three entries; targeted edits only):

- **GAP-20260424-030** — Status: `OPEN` → `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records §6 resolution with per-candidate `break_even_rule` provenance and future-runtime guardrail. Resolution evidence: Phase 3w memo. Related docs extended.
- **GAP-20260424-031** — Status: `OPEN` → `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records §7 resolution with per-candidate `ema_slope_method` provenance and future-runtime guardrail. Resolution evidence: Phase 3w memo. Related docs extended.
- **GAP-20260424-033** — Status: `OPEN` → `RESOLVED — Phase 3w governance memo (2026-04-30)`. Operator decision records §8 resolution with per-candidate `stagnation_window_role` provenance and future-runtime guardrail. Resolution evidence: Phase 3w memo. Related docs extended.

After these updates, `docs/00-meta/implementation-ambiguity-log.md` has **zero OPEN entries** that constitute pre-coding blockers per Phase 3u §8.5. Pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED`) remain as documented in the ambiguity log and `docs/12-roadmap/technical-debt-register.md`.

## Commit

- **Phase 3w memo + ambiguity-log update commit:** `29054ce8a0cc43854283e96c802e549531e0ae7d` — `phase-3w: remaining ambiguity-log resolution memo (docs-only)`.
- **This closeout-file commit:** the next commit on the `phase-3w/remaining-ambiguity-log-resolution` branch, advancing past `29054ce`. Its SHA is reported in the chat closeout block accompanying this commit.

Phase 3w branch tip before this closeout-file commit: `29054ce8a0cc43854283e96c802e549531e0ae7d`.

## Final git status

```text
clean
```

Working tree empty after this closeout-file commit. No uncommitted changes. No untracked files.

## Final git log --oneline -5

Snapshot at this closeout-file commit:

```text
<recorded after this closeout-file itself is committed>  docs(phase-3w): closeout report (Markdown artefact)
29054ce  phase-3w: remaining ambiguity-log resolution memo (docs-only)
fdbbfab  docs(phase-3v): merge closeout + current-project-state sync
15ba71c  Merge Phase 3v (docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo) into main
5be9978  docs(phase-3v): closeout report (Markdown artefact)
```

The closeout-file commit's own SHA cannot be embedded in itself (the inherent self-reference limit, consistent with prior phases' closeouts); it is reported in the chat closeout block accompanying this commit.

## Final rev-parse

- **`git rev-parse HEAD`** (Phase 3w branch tip after this closeout-file commit): reported in the chat closeout block accompanying this commit.
- **`git rev-parse phase-3w/remaining-ambiguity-log-resolution`** (local): same as `HEAD` above.
- **`git rev-parse origin/phase-3w/remaining-ambiguity-log-resolution`** (after push): same as `HEAD` above.
- **`git rev-parse main`**: `fdbbfabfc935fb9dfb521250d3dcb4e711216be6` (unchanged).
- **`git rev-parse origin/main`**: `fdbbfabfc935fb9dfb521250d3dcb4e711216be6` (unchanged).
- **`git rev-parse origin/phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7` (unchanged).
- **`git rev-parse origin/phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (unchanged).
- **`git rev-parse origin/phase-3t/post-5m-diagnostics-consolidation`**: `fcf8192e150e7dc783da345d2e54be8cff1611db` (unchanged).
- **`git rev-parse origin/phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a` (unchanged).
- **`git rev-parse origin/phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (unchanged).
- **`git rev-parse origin/phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (unchanged).

## Branch / main status

- Phase 3w branch `phase-3w/remaining-ambiguity-log-resolution` is pushed to origin and tracking remote.
- Phase 3w is **not merged to main**.
- All prior phase branches preserved at their respective tips.
- main = origin/main = `fdbbfabfc935fb9dfb521250d3dcb4e711216be6` (unchanged from the post-Phase-3v-merge housekeeping commit).
- Operator review pending. The brief explicitly required "Do not merge to main unless explicitly instructed."

## Forbidden-work confirmation

- **No Phase 4 / Phase 4a started.** Phase 3w recommends Phase 4 remain unauthorized and Phase 4a remain conditional only.
- **No implementation code written.** Phase 3w is text-only (memo + ambiguity-log entry edits).
- **No runtime / strategy / execution / risk-engine / database / dashboard / exchange code modified.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No Q1–Q7 rerun.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No H-D3 / H-C2 / H-D5 sensitivity analysis.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. **§11.6 unchanged.** **§1.7.3 unchanged.**
- **No Phase 3v §8 stop-trigger-domain rule modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.** Spec lines 156–172, 380, 415, 564 all preserved verbatim.
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No strategy rescue proposal.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, or 5m-on-X variant.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket subscription.**
- **No public endpoints consulted.** Phase 3w performs no network I/O.
- **No secrets requested or stored.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a (safe slice) remains conditional only and not authorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8.
- **Break-even rule governance:** RESOLVED by Phase 3w §6.
- **EMA slope method governance:** RESOLVED by Phase 3w §7.
- **Stagnation window role governance:** RESOLVED by Phase 3w §8.
- **OPEN ambiguity-log items after Phase 3w:** zero relevant to Phase 4a / runtime / strategy implementation. All four Phase 3u §8.5 currently-OPEN pre-coding blockers RESOLVED at the governance level.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-3w/remaining-ambiguity-log-resolution` pushed at `29054ce` (advanced by this closeout-file commit); not merged.
  - All prior phase branches preserved at their respective tips.
  - main = origin/main = `fdbbfab` unchanged.

## Next authorization status

**No next phase has been authorized.** Phase 3w recommends Option A (remain paused) as primary; Option B (Phase 4a safe-slice scoping memo per Phase 3u §16.3 + Phase 3v §17.3) as conditional secondary subject to Phase 3u §10 anti-live-readiness preconditions; Option C (sensitivity analyses on retained-evidence populations: H-D3 / H-C2 / H-D5 / mark-price-stop) as conditional alternative not recommended now (low expected new information; high procedural cost); Options D (fresh-hypothesis research) and E (Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write) NOT recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
