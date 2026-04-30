# Phase 3r Closeout

## Summary

Phase 3r (docs-only) produced the mark-price gap governance memo formalizing how known upstream `data.binance.vision` maintenance-window gaps in the Phase 3q v001-of-5m mark-price datasets must be handled if a future Q1–Q7 diagnostics-execution phase is ever authorized. Operator selected Phase 3p §10 / Phase 3q decision menu Option B: a docs-only governance decision *before* any potential diagnostics-execution.

**Recommendation: Option B (known-invalid-window exclusion for Q6 only)** as primary. Phase 3p §4.7 strict integrity gate stays unchanged. Mark-price 5m datasets remain `research_eligible: false`. The Phase 3q manifests are not modified. The four gap windows remain exclusion zones, not patch zones. Phase 3r §8 specifies a full normative Q6 invalid-window exclusion rule (no forward-fill / interpolation / imputation / replacement; per-trade exclusion test; excluded counts reported by candidate / symbol / side / exit-type / gap-window; Q6 outputs labeled conditional on valid mark-price coverage; no automatic prior-verdict revision; no strategy rescue / parameter change / live-readiness implication; no silent rule revision) that any future Q6-running phase must obey.

**Q6 disposition:** bounded-conditional optionality. Q6 stays on the menu but only as a §8-bounded option. Q6 is NOT permanently retired. Q6 is NOT currently authorized.

**Q1 / Q2 (trade-price base) / Q3 / Q4 / Q5 / Q7 unaffected.** Trade-price 5m datasets remain research-eligible. Q4 uses v002 funding events.

**No diagnostics run. No Q1–Q7 answered. No backtests. No prior-verdict / threshold / project-lock / strategy-parameter modification. No data acquisition. No data modification. No manifest modification. No Phase 3p §4.7 amendment.** Phase 3r authorizes nothing other than the in-memo §8 governance rule itself, which is forward-binding on any future Q6-running phase but does not start such a phase. **Phase 3r is not merged. No successor phase has been authorized.**

## Files changed

Phase 3r memo branch (`phase-3r/mark-price-gap-governance`) committed two files; both new, both under `docs/00-meta/implementation-reports/`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-3r_mark-price-gap-governance-memo.md` — Phase 3r governance memo (14 sections covering Summary; Authority and boundary; Starting state; Phase 3q evidence recap; Governance problem; Options considered (A–E); Recommended governance decision; Formal rule for invalid-window handling (§8); Q6 disposition; Effect on Q1 / Q2 / Q3 / Q5 / Q7; What remains forbidden; Prior-verdict and lock preservation; Operator decision menu; Next authorization status). Committed at `0082488`.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3r_closeout.md` — this closeout file. Committed in this commit on the Phase 3r branch.

NOT modified (preserved verbatim):

- `docs/00-meta/implementation-reports/2026-04-30_phase-3p_5m-diagnostics-data-requirements-and-execution-plan.md` — Phase 3p §4.7 NOT amended.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3q_5m-data-acquisition-and-integrity-validation.md` — Phase 3q evidence preserved.
- `docs/00-meta/implementation-reports/2026-04-30_phase-3q_closeout.md` — Phase 3q closeout preserved.
- `docs/00-meta/current-project-state.md` — no Phase 3r line added (Phase 3r is not merged; no current-state update appropriate at branch-state).
- All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m) — untouched.
- All `data/raw/**` and `data/normalized/**` partitions — untouched.
- All `src/prometheus/**` source — untouched.
- All `scripts/**` — untouched.
- All `tests/**` — untouched.
- All `.claude/rules/**` — untouched.

## Governance decision

Phase 3r adopts **Option B** as the recommended governance posture:

- Phase 3p §4.7 strict integrity gate stays unchanged.
- Mark-price 5m datasets remain `research_eligible: false` in their manifests.
- No data is patched, forward-filled, interpolated, imputed, or replaced.
- Q6 is conditionally permitted *if* a future diagnostics-execution phase is separately authorized, under the binding **Q6 invalid-window exclusion rule** specified in Phase 3r §8.
- Q6 outputs must drop every trade whose Q6 analysis window intersects a known invalid window, report excluded counts by candidate / symbol / side / exit-type / gap-window, label all Q6 conclusions "conditional on valid mark-price coverage," and never revise prior verdicts, change parameters, rescue candidates, or imply anything about live-readiness.
- The §8 rule is itself predeclared and immutable from the Phase 3r commit forward.

Options A (drop Q6 permanently), C (amend §4.7), D (seek alternative source), E (drop Q6 permanently — Option E variant) are evaluated but not recommended. Phase 3r preserves §4.7 verbatim.

## Q6 disposition

| Aspect | Disposition |
|---|---|
| **Permanently retired?** | No. Q6 stays on the menu. |
| **Currently authorized?** | No. Phase 3r authorizes nothing. |
| **Conditionally permitted in a future phase?** | Yes — *only* under Phase 3r §8. |
| **Prior-verdict revision allowed by Q6?** | Never. |
| **Strategy rescue / parameter change allowed by Q6?** | Never. |
| **Live-readiness / Phase 4 / paper/shadow implication allowed by Q6?** | Never. |
| **Forward-fill / interpolation / imputation / patch allowed?** | Never. |
| **Excluded-trade count reporting required if Q6 is run?** | Yes. By candidate / symbol / side / exit-type / gap-window. |
| **Q6 output labeling required?** | Yes. "Conditional on valid mark-price coverage" or equivalent must accompany every Q6 conclusion. |

## Commit

- **Phase 3r memo commit:** `0082488c3238fcd35330603b7a4d08601771f79c` — `phase-3r: mark-price gap governance memo (docs-only)`.
- **Phase 3r closeout commit (this commit):** the next commit on the `phase-3r/mark-price-gap-governance` branch, advancing past `0082488`. Its SHA is reported in the chat closeout block accompanying this commit.

Phase 3r branch tip before this closeout-file commit: `0082488c3238fcd35330603b7a4d08601771f79c`.

## Final git status

```text
clean
```

Working tree empty after this closeout-file commit. No uncommitted changes. No untracked files.

## Final git log --oneline -5

Snapshot at this closeout-file commit:

```text
<recorded after this closeout-file itself is committed>  docs(phase-3r): closeout report (Markdown artefact)
0082488  phase-3r: mark-price gap governance memo (docs-only)
3078b44  docs(phase-3q): closeout report (Markdown artefact replacing chat-only closeout)
8d99375  phase-3q: 5m data acquisition + integrity validation (docs-and-data, partial pass)
9428b05  docs(phase-3p): merge closeout + current-project-state sync
```

The closeout-file commit's own SHA cannot be embedded in itself (the inherent self-reference limit, consistent with prior phases' closeouts); it is reported in the chat closeout block accompanying this commit.

## Final rev-parse

- **`git rev-parse HEAD`** (Phase 3r branch tip after this closeout-file commit): reported in the chat closeout block accompanying this commit.
- **`git rev-parse phase-3r/mark-price-gap-governance`** (local): same as `HEAD` above.
- **`git rev-parse origin/phase-3r/mark-price-gap-governance`** (after push): same as `HEAD` above.
- **`git rev-parse main`**: `9428b05044d57dbd3a1a5739a2b8b1db418dcade` (unchanged).
- **`git rev-parse origin/main`**: `9428b05044d57dbd3a1a5739a2b8b1db418dcade` (unchanged).
- **`git rev-parse origin/phase-3q/5m-data-acquisition-and-integrity-validation`**: `3078b448e5850f943079899c9048b2c19e07adb3` (unchanged).

## Branch / main status

- Phase 3r branch `phase-3r/mark-price-gap-governance` is pushed to origin and tracking remote.
- Phase 3r is **not merged to main**.
- Phase 3q branch `phase-3q/5m-data-acquisition-and-integrity-validation` remains pushed at `3078b44`, **not merged to main**.
- main = origin/main = `9428b05044d57dbd3a1a5739a2b8b1db418dcade` (unchanged from the post-Phase-3p housekeeping commit).
- Operator review pending. The brief explicitly required "Do not merge to main unless explicitly instructed."

## Forbidden-work confirmation

- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question answered. No diagnostic table, plot, or classification produced.
- **No Q1–Q7 answers.** Q6 is conditionally permitted in a future phase under §8; nothing about Phase 3r constitutes that authorization.
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No control rerun.
- **No data acquisition / download / patch / regeneration / modification.** Phase 3r consulted no Binance endpoint, downloaded nothing, patched nothing.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) untouched.
- **No v002 dataset / manifest modification.** v002 partitions and manifests untouched.
- **No mark-price 5m manifest re-issue.** `research_eligible: false` flag remains on both `binance_usdm_btcusdt_markprice_5m__v001.manifest.json` and `binance_usdm_ethusdt_markprice_5m__v001.manifest.json`. NOT flipped to `true`.
- **No Phase 3p text modification.** Phase 3r is a new governance memo; Phase 3p §4.7 stands as-written.
- **No strategy / parameter / threshold / project-lock / prior-verdict modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **No 5m strategy / hybrid / variant created.**
- **No diagnostics-execution started.**
- **No Phase 4 / paper/shadow / live-readiness / deployment / production-key / exchange-write paths touched.**
- **No private Binance endpoints / user stream / WebSocket.** No public endpoints consulted either; Phase 3r is text-only.
- **No MCP / Graphify / `.mcp.json` / credentials.**
- **No secrets requested or stored.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Phase 3o predeclared Q1–Q7 + forbidden forms + diagnostic terms + analysis boundary; Phase 3p added data-requirements + dataset-versioning approach + manifest specification + per-question outputs + outcome-interpretation rules; Phase 3q acquired the 5m datasets and ran integrity checks (trade-price PASS, mark-price FAIL strict gate); Phase 3r added the mark-price gap governance memo (Option B + §8 Q6 invalid-window exclusion rule). The thread now has a complete, predeclared, immutable specification covering questions, data, governance, and outcome-interpretation. Whether to *act on* the specification is a separate operator-strategic decision.
- **Trade-price 5m datasets:** locally research-eligible; Q1, Q2 (trade-price-side), Q3, Q4, Q5 unaffected by Phase 3r §8.
- **Mark-price 5m datasets:** NOT research-eligible under Phase 3p §4.7 strict gate. Q6 is conditionally permitted under Phase 3r §8 *only*.
- **Project locks preserved verbatim.** §1.7.3 mark-price-stops policy preserved.
- **Branch state:**
  - `phase-3q/5m-data-acquisition-and-integrity-validation` pushed at `3078b44`; not merged.
  - `phase-3r/mark-price-gap-governance` pushed at the SHA reported in the chat closeout; not merged.
  - main = origin/main = `9428b05` unchanged.

## Next authorization status

**No next phase has been authorized.** Phase 3r stops here for operator review. Phase 3r recommends Option A (adopt §8; remain paused) as primary; Option B (adopt §8 AND authorize a future docs-only diagnostics-execution phase, with operator-explicit Q6 disposition) as conditional secondary. Options C (run Q6 only), D (combine §8 with §4.7 amendment), E (reject Phase 3r and permanently retire Q6), F (strategy rescue / Phase 4 / paper/shadow / live-readiness / deployment) are NOT recommended. Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
