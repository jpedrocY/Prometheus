# Phase 3s Merge Closeout

## Summary

Phase 3s — the **5m diagnostics execution phase** that ran the predeclared Phase 3o / Phase 3p Q1–Q7 question set exactly once on the v002-locked retained-evidence trade populations using Phase 3q v001-of-5m supplemental datasets and the Phase 3r §8 Q6 invalid-window exclusion rule — has been merged to `main` and pushed to `origin/main`.

**Q1, Q2, Q3 (+1R), Q6 (D1-A only), and Q7 meta classified informative.** **Q4 and Q5 classified non-informative.** **Q3 +2R ambiguous.** Phase 3r §8 exclusion rule applied verbatim with **zero trades excluded empirically** (retained-evidence trade lifetimes ≤ 8 h too short to straddle the four mark-price gap windows; rule remains binding for any future Q6-running phase).

Headline findings (all descriptive-only, all bound by Phase 3o §6 / §10 + Phase 3p §8 + Phase 3r §8 prohibitions):

- **Q1 (informative):** Universal entry-path adverse bias — IAE > IFE in 7 of 8 candidate × symbol cells. F1 most pronounced (~0.5 R consumed in first 5 min); R3 / R2 / D1-A also show adverse-leaning first-5min path.
- **Q2 (informative):** Cleanest cross-family mechanism finding. V1-family (R3, R2) wick-dominated stop pathology (wick-fraction 0.571–1.000); F1 + D1-A sustained-dominated stop pathology (wick-fraction 0.269–0.347). Both directions of differential meet Phase 3p §8.2 thresholds.
- **Q3 (informative for +1R; ambiguous for +2R):** +1R intrabar-touch fraction in adverse-exit trades ≥ 25% in 6 of 8 cells (R2 BTC 47.8%, R2 ETH 47.4%, R3 ETH 45.5%, D1-A BTC 35.6%, D1-A ETH 34.6%, R3 BTC 27.3%; F1 just below at 23.6% / 24.0%). +2R fractions uniformly low. **Phase 3p §8.3 critical: descriptive-only; cannot license rule revision; Phase 3o §6.3 forbidden-question prohibition preserved.**
- **Q4 (non-informative):** D1-A funding-decay curve has no monotone shape; SEM bands wider than displacement magnitudes on both BTC and ETH. Phase 3p §8.4 noise-floor predicate fails on both symbols.
- **Q5 (non-informative):** No cell has |signed slippage mean| > 8 bps. F1 (-3.71 / -4.18 bps), D1-A (-2.91 / -2.91 bps) tilt slightly toward 15m assumption being unfavorable, but well below threshold. Consistent with Phase 3l "B — conservative but defensible". §11.6 = 8 bps HIGH per side preserved.
- **Q6 (informative for D1-A only):** D1-A mark-stops trigger ~1.3–1.8 5m bars **after** trade-stops would (BTC mean +1.252; ETH mean +1.783). Both symbols exceed 1-bar threshold; cross-symbol replicable. R3 / R2 / F1 mark-vs-trade timing within 1 bar (non-informative). All Q6 conclusions labeled "conditional on valid mark-price coverage" per Phase 3r §8.5.
- **Q7 (informative):** Meta-classification per Phase 3p §8.7. 4 of 6 Q1–Q6 informative ≥ 3-threshold met. The diagnostic phase produced a coherent body of informative findings, not just isolated signals.

**The four findings (Q1 / Q2 / Q3 / Q6) are descriptive only and cannot revise verdicts or authorize strategy rescue, parameter change, threshold revision, project-lock revision, 5m strategy / hybrid / variant proposal, paper/shadow planning, Phase 4, live-readiness, deployment, or any successor authorization.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim. **5m research thread is operationally complete.** Recommended state remains **paused**. **No successor phase has been authorized.**

## Files changed

The Phase 3s merge into `main` brought in five new files (the Phase 3s artefacts that previously existed only on the Phase 3s branch):

- `scripts/phase3s_5m_diagnostics.py` — standalone diagnostics script (672 lines). Reads only existing v002 retained-evidence `trade_log.parquet` artefacts and Phase 3q 5m parquet partitions. No Interval-enum extension. No `prometheus.research.data.*` modification. No backtest. No data acquisition.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3s_5m-diagnostics-execution.md` — Phase 3s diagnostics-execution report (558 lines).
- `docs/00-meta/implementation-reports/2026-04-30_phase-3s_closeout.md` — Phase 3s closeout artefact (171 lines).
- `docs/00-meta/implementation-reports/phase-3s/q1_q5_results.json` — auditable raw diagnostic statistics per (candidate, symbol, question) (809 lines).
- `docs/00-meta/implementation-reports/phase-3s/q6_exclusion_counts.json` — Phase 3r §8 exclusion-counts table (empty list: zero exclusions).

Total Phase 3s merge: 5 files added, 2 211 insertions.

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3s_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 3s merged, Q1–Q7 verdict summary, Phase 3r §8 zero-exclusion finding, 5m research thread operationally complete, recommended state paused, no next phase authorized. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 3s merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files (v002 manifests + Phase 3q v001-of-5m manifests; mark-price `research_eligible: false` flag preserved).
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions (git-ignored per repo convention; v002 partitions and Phase 3q 5m partitions untouched on local filesystem).
- All `src/prometheus/**` source code (Interval enum NOT extended).
- All other scripts under `scripts/` (only `phase3s_5m_diagnostics.py` is new).
- All `tests/**`.
- All `.claude/rules/**`.
- Phase 3o / 3p / 3q / 3r reports / closeouts / merge-closeouts (predeclared rules and prior boundaries preserved verbatim).

## Diagnostics commits included

| Commit | Subject |
|---|---|
| `af7a95ba2402b8ba2298c75ec884a6847cd04b18` | `phase-3s: 5m diagnostics execution (diagnostics-and-reporting)` — Phase 3s diagnostics script + execution report + raw outputs. |
| `a93695f23d78f8975f33211439d66f8e5c90b49a` | `docs(phase-3s): closeout report (Markdown artefact)` — Phase 3s closeout. |

## Merge commit

- **Phase 3s merge commit (`--no-ff`, ort strategy):** `3f6e015a7a0fc9263dbd7e4f60ff690cbab83042`
- **Merge title:** `Merge Phase 3s (5m diagnostics execution Q1-Q7 once with Phase 3r §8 exclusion rule applied) into main`

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 3s merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `3f6e015` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern, the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-3s): merge closeout + current-project-state sync
3f6e015  Merge Phase 3s (5m diagnostics execution Q1-Q7 once with Phase 3r §8 exclusion rule applied) into main
a93695f  docs(phase-3s): closeout report (Markdown artefact)
af7a95b  phase-3s: 5m diagnostics execution (diagnostics-and-reporting)
f20c0ed  docs(phase-3r): merge closeout + current-project-state sync
3cf2ba2  Merge Phase 3r (docs-only mark-price gap governance memo + Phase 3q acquisition evidence) into main
0611195  docs(phase-3r): closeout report (Markdown artefact)
0082488  phase-3r: mark-price gap governance memo (docs-only)
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a` (branch tip preserved).
- **`git rev-parse origin/phase-3s/5m-diagnostics-execution`**: `a93695f23d78f8975f33211439d66f8e5c90b49a`.
- **`git rev-parse phase-3r/mark-price-gap-governance`**: `06111957e465a4fc5d59190d82db379cc0f7cc86` (branch tip preserved).
- **`git rev-parse phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (branch tip preserved).

## main == origin/main confirmation

After the Phase 3s merge push: local `main` = `origin/main` = `3f6e015a7a0fc9263dbd7e4f60ff690cbab83042`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## Q1–Q7 verdict summary

| Question | Verdict | Phase 3p §8 rule applied |
|---|---|---|
| **Q1** — IAE/IFE first 5–15 min after entry | **Informative** | §8.1: IAE > IFE in 7 of 8 cells; cross-symbol replicable; mechanism-coherent. |
| **Q2** — Wick-stop vs sustained-stop | **Informative** | §8.2: V1-family wick-fraction ≥ 60% threshold met (R3 BTC 0.833, R3 ETH 0.636, R2 BTC 1.000, R2 ETH 0.571); F1 + D1-A wick-fraction ≤ 40% threshold met (0.269–0.347). Both directions of differential informative. |
| **Q3 (+1R)** — Intrabar +1R target touches | **Informative** | §8.3: 6 of 8 cells ≥ 25% threshold; cross-symbol replicable for R2, D1-A. **Critical: descriptive-only; cannot license rule revision; Phase 3o §6.3 forbidden-question prohibition preserved.** |
| **Q3 (+2R)** — Intrabar +2R target touches | **Ambiguous** | §8.3: All cells well below typical informativeness; F1 strikingly low (0.048 / 0.052). |
| **Q4** — D1-A funding decay | **Non-informative** | §8.4: No monotone shape; SEM > displacement magnitude on both BTC and ETH at the 60-min milestone. |
| **Q5** — 15m-vs-5m fill realism | **Non-informative** | §8.5: No |signed mean| > 8 bps cell. Consistent with Phase 3l "B — conservative but defensible". §11.6 preserved. |
| **Q6** — Mark-vs-trade stop trigger | **Informative for D1-A only; non-informative for R3 / R2 / F1; conditional on valid mark-price coverage per Phase 3r §8.5** | §8.6: D1-A BTC mean +1.252 5m-bars, D1-A ETH mean +1.783 5m-bars; both > 1-bar threshold; cross-symbol replicable. R3 / R2 / F1 timings within 1 bar. |
| **Q7** — Meta-classification | **Informative** | §8.7: 4 of 6 informative ≥ 3-threshold met. The diagnostic phase produced a coherent body of informative findings. |

**Findings are descriptive only.** Phase 3p §8 critical reminders (§8.1 / §8.2 / §8.3 / §8.5 / §8.6), Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, Phase 3r §8 Q6 invalid-window exclusion rule all preserved. The findings cannot revise verdicts (R3 baseline-of-record; R2 FAILED; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other), change parameters, revise thresholds, revise project-locks, license stop-policy revision (mark-price stops locked by §1.7.3), or authorize any strategy / hybrid / variant / successor / 5m / paper-shadow / Phase 4 / live-readiness / deployment work.

## Q6 exclusion summary

Phase 3r §8 Q6 invalid-window exclusion rule applied verbatim:

| Population | Symbol | Applicable (STOP-exited) | Excluded by §8 | Included | Inconclusive 5m trigger | Mean (mark − trade) bars |
|---|---|---|---|---|---|---|
| R3 | BTC | 8 | 0 | 8 | 0 | +0.125 |
| R3 | ETH | 14 | 0 | 14 | 0 | +0.286 |
| R2 | BTC | 6 | 0 | 6 | 0 | 0.000 |
| R2 | ETH | 10 | 0 | 10 | 0 | +0.400 |
| F1 | BTC | 2 534 | 0 | 2 531 | 3 | +0.373 |
| F1 | ETH | 2 516 | 0 | 2 516 | 0 | +0.353 |
| D1-A | BTC | 135 | 0 | 135 | 0 | **+1.252** |
| D1-A | ETH | 120 | 0 | 120 | 0 | **+1.783** |
| **TOTAL** | | **5 343** | **0** | **5 336** | **7** | |

**Phase 3r §8 exclusion-counts table:** empty (zero exclusions). The §8 rule was applied verbatim — predeclared, immutable, audited — and verified to not exclude any retained-evidence trade in the empirical data. The rule remains binding for any future Q6-running phase regardless.

The four mark-price gap windows (BTC: 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10) total ~4 425 min (BTC) / ~2 990 min (ETH). Retained-evidence trade lifetimes (R3 / R2 ≤ 2 h; F1 ≤ 2 h; D1-A ≤ 8 h) are short relative to the gap windows; no trade lifetime intersected any gap window in the empirical data.

## Strategic interpretation

### What the findings tell us about why retained-evidence candidates failed framework discipline

- **V1-family (R3, R2) wick-stop pathology:** Stops sit in a wick-vulnerable zone. Stops trigger frequently on 5m wicks that close back inside the position-favorable side. The broader breakout-continuation thesis is *not categorically refuted* by Q2; the failure mode is at the stop-placement layer.
- **F1 / D1-A sustained-stop pathology:** Stops trigger because the underlying impulse continued in the entry-adverse direction for ≥ 3 × 5m bars. The mean-reversion / contrarian thesis didn't materialize in time. **This is a *signal-failure* signature.** The thesis itself doesn't hold often enough.
- **Q1 universal adverse bias:** All four candidates show a structural first-5-min adverse path bias after completed-15m-bar entries. This affects every retained-evidence family.

### What the findings explicitly do NOT tell us

- They do not provide a path to rescue R2 (still FAILED on §11.6 cost-sensitivity).
- They do not provide a path to rescue F1 (still HARD REJECT on catastrophic-floor predicate).
- They do not provide a path to rescue D1-A (still MECHANISM PASS / FRAMEWORK FAIL — other).
- They do not provide a path to revise R3 baseline-of-record.
- They do not provide a path to authorize a 5m strategy / hybrid / D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid.
- They do not provide a path to revise §11.6 = 8 bps HIGH per side (Q5 confirms current cost model).
- They do not provide a path to revise mark-price stop policy (§1.7.3 locked; Q6 finding is descriptive only).
- They do not provide a path to authorize regime-first formal spec, ML feasibility, or new strategy-family discovery.
- They do not provide a path to authorize paper/shadow, Phase 4, live-readiness, deployment, production-key creation, or exchange-write capability.

### Answers to the four originally-unresolved strategic questions (per Phase 3n §3 framing)

| Question | Phase 3s answer |
|---|---|
| Are we missing useful timing information inside 15m bars? | **Yes — but cannot be acted on under predeclared rules.** |
| Can regimes be defined cleanly before testing, without overfitting? | **Out of scope.** Phase 3s did not test; Phase 3m's regime-first caution still applies. |
| Would more granular data help diagnostics, or just increase noise/cost? | **Mostly increases noise/cost.** 5m is sufficient; finer granularity not recommended. |
| Is there a truly new hypothesis strong enough to deserve implementation? | **No.** Informative findings ≠ strategy candidates. |

## Forbidden-work confirmation

- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No control rerun.
- **No retained-evidence trade population regenerated.** All four canonical runs read read-only from existing artefacts.
- **No v002 dataset / manifest modification.** v002 partitions and manifests untouched.
- **No Phase 3q v001-of-5m manifest modification.** Mark-price `research_eligible: false` preserved.
- **No v003 created.**
- **No data acquisition / download / patch / regeneration / modification.** Phase 3s is read-only on data; the merge brings in pre-existing Phase 3s artefacts unchanged.
- **No forward-fill / interpolation / imputation / replacement / synthetic data.** Phase 3r §8 prohibition applied verbatim throughout Phase 3s and preserved in the merge.
- **No strategy / parameter / threshold / project-lock / prior-verdict modification.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **No verdict revision.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant proposal.** Phase 3o §4.1 / Phase 3p §10 prohibition preserved.
- **No Q1–Q7 rerun.**
- **No new diagnostics.**
- **No Phase 4 / paper-shadow / live-readiness / deployment / production-key / exchange-write paths touched.**
- **No MCP / Graphify / `.mcp.json` / credentials.**
- **No private Binance endpoints / user stream / WebSocket subscription / public endpoints consulted.** This merge + housekeeping commit performs no network I/O.
- **No secrets requested or stored.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `3f6e015`. Phase 3s diagnostics evidence consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** **Operationally complete.** Phase 3o predeclared questions; Phase 3p added data requirements + dataset-versioning + manifest specification + per-question outputs + outcome-interpretation rules; Phase 3q acquired data + ran integrity checks (trade-price PASS, mark-price FAIL strict gate); Phase 3r added mark-price gap governance + §8 Q6 invalid-window exclusion rule; Phase 3s executed Q1–Q7 once with Phase 3p §8 classifications applied. The thread has produced its complete output. Running anything further would either repeat the same questions on alternative populations (low marginal value) or extend into forbidden territory (high risk).
- **Project locks preserved verbatim.**
- **Branch state:**
  - `phase-3s/5m-diagnostics-execution` pushed at `a93695f`. Its commits are now reachable from `main` via the Phase 3s merge ancestry.
  - `phase-3r/mark-price-gap-governance` pushed at `0611195`. Its commits are reachable from `main` via the prior Phase 3r merge.
  - `phase-3q/5m-data-acquisition-and-integrity-validation` pushed at `3078b44`. Its commits are reachable from `main` via the prior Phase 3r merge.

## Next authorization status

**No next phase has been authorized.** Phase 3s recommended Option A (remain paused) as primary; Option B (docs-only post-Phase-3s consolidation memo) as conditional secondary subject to explicit anti-rescue preconditions; Options C–F (5m strategy / hybrid / successor / regime-first formal spec / ML feasibility / new strategy-family discovery / paper-shadow / Phase 4 / live-readiness / deployment) NOT recommended. Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
