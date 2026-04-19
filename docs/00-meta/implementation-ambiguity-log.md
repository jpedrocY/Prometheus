# Implementation Ambiguity Log

## Purpose

This log records ambiguities, specification gaps, doc/disk inconsistencies, unclear API behavior, and pending implementation decisions discovered by Claude Code during phased implementation of Prometheus.

Entries are not issues to be silently patched. They are decisions or questions that deserve operator or ChatGPT review before they shape live-relevant behavior.

This log complements `docs/12-roadmap/technical-debt-register.md`. Safety-relevant open items should also be reflected there. This log is where items are first captured; the debt register is where they graduate if they remain open across phases.

## Entry format

```
## GAP-YYYYMMDD-NNN — Short title

Status:              OPEN | IN_REVIEW | RESOLVED | ACCEPTED_LIMITATION | SUPERSEDED
Phase discovered:    0 | 1 | 2 | ...
Area:                DOCS | TOOLING | STRATEGY | DATA | RISK | EXECUTION | ARCHITECTURE | OPERATIONS | SECURITY | INTERFACE | OTHER
Blocking phase:      NON_BLOCKING | PRE_CODING_START | PRE_DRY_RUN | PRE_PAPER_SHADOW | PRE_TINY_LIVE | PRE_SCALED_LIVE | POST_MVP | FUTURE_RESEARCH
Risk level:          LOW | MEDIUM | HIGH | CRITICAL
Related docs:        <paths>

Description:
<what was found>

Why it matters:
<consequence if ignored>

Options considered:
- Option A: ...
- Option B: ...

Recommended resolution:
<claude code's recommendation>

Operator decision:
<filled by operator or "pending">

Resolution evidence:
<commit hash / file path / command output once resolved>
```

---

## GAP-20260419-001 — Filename mismatch: `first_strategy-comparison.md` vs `first-strategy-comparison.md`

Status:              RESOLVED
Phase discovered:    0 (repository audit)
Area:                DOCS
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/03-strategy-research/first-strategy-comparison.md`, `README.md`, `docs/00-meta/current-project-state.md`, `docs/05-backtesting-validation/cost-modeling.md`

Description:
The on-disk filename was `docs/03-strategy-research/first_strategy-comparison.md` (underscore), while `README.md:243` and `docs/00-meta/current-project-state.md:366` referenced the dashed form `first-strategy-comparison.md`. `docs/05-backtesting-validation/cost-modeling.md:45` contains the natural-language phrase "first strategy comparisons" and is unaffected.

Why it matters:
Broken path references cause confusion during documentation reading and tool indexing, and cost-modeling's natural-language phrase was not part of the inconsistency. The mismatch is documentation-only and does not touch runtime safety, but was logged to leave a clean audit trail of the Phase 1 rename.

Options considered:
- Option A: rename file on disk to match docs (dashed form).
- Option B: edit both docs to match the on-disk underscore form.

Recommended resolution:
Option A — rename `first_strategy-comparison.md` → `first-strategy-comparison.md` using `git mv` (preserves history). After rename, both existing doc references become correct without further edits.

Operator decision:
Approved at Phase 1 gate-1 approval (2026-04-19). Option A.

Resolution evidence:
Rename applied via `git mv` in Phase 1 Step 2 on branch `phase-1/local-dev-foundation`. Will be included in the Phase 1 "docs: rename ..." commit after gate-2 approval.

---

## GAP-20260419-002 — Phase 1 tooling decisions confirmed

Status:              RESOLVED
Phase discovered:    1 (local development foundation)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/00-meta/ai-coding-handoff.md` §"Phase 1", `docs/08-architecture/codebase-structure.md`

Description:
Phase 1 requires decisions that were not pre-specified in the handoff: package manager, Python version pin, dev-dependency mechanism, pre-commit/CI scoping. Operator approved each choice explicitly.

Decisions (2026-04-19):
- Package manager: `uv`.
- Python version policy: `>=3.11,<3.13`. Actual pin determined by the interpreter detected in Step 0 pre-flight.
- Pinned `.python-version`: `3.12` (host reports Python 3.12.4).
- Dev dependencies: PEP 735 `[dependency-groups]` in `pyproject.toml` (not `[project.optional-dependencies]`), installed automatically by `uv sync`.
- Pre-commit hooks: deferred. Tooling config in `pyproject.toml` only; no hook install.
- CI (GitHub Actions): deferred to the end of Phase 1; proposed separately once local ruff/mypy/pytest pass.
- Branching: feature branch `phase-1/local-dev-foundation` off `main`. Commits reviewed at Gate 2 before any `git commit`.
- Commit messages: no `Co-Authored-By` trailer unless explicitly requested later.

Why it matters:
These choices shape every subsequent phase. Recording them here gives future phases (and future audits) a single place to check what was decided and when, without spelunking through commit history.

Options considered:
See plan file `C:\Users\jpedr\.claude\plans\approved-to-start-phase-bubbly-whisper.md` §14 and §J for the alternatives weighed.

Recommended resolution:
As decided above.

Operator decision:
Approved 2026-04-19 with corrections (gate-1 corrections J.1–J.3 in the plan file).

Resolution evidence:
- `pyproject.toml` with `[dependency-groups] dev = [...]`.
- `.python-version` pinned to `3.12`.
- `uv.lock` generated by `uv sync`.
- Quality gates pass in Phase 1 Step 11.

---

## GAP-20260419-003 — `.python-version` was git-ignored; narrow `.gitignore` edit authorized

Status:              RESOLVED
Phase discovered:    1 (local development foundation, Step 5)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `.gitignore`, `pyproject.toml`, `docs/08-architecture/codebase-structure.md`

Description:
During Phase 1 Step 5, the intended commit of the root `.python-version` file was blocked because `.gitignore:16` excluded the pattern `.python-version` (under a `# Python` section alongside `__pycache__/`, `*.py[cod]`, `.venv/`, etc.). This prevented deterministic reproduction of the interpreter version by uv on fresh clones.

Why it matters:
`.python-version` is the first-class signal uv (and pyenv) read to select the project's Python interpreter. Without committing it, each contributor's environment is determined only by the broader `requires-python = ">=3.11,<3.13"` bound in `pyproject.toml`, which allows silent drift across 3.11/3.12 patch versions and leaves no single shared pin.

Options considered:
- Option A: remove the `.python-version` line from `.gitignore` (simplest, matches uv-first workflow).
- Option B: add `!/.python-version` as an explicit unignore rule at the bottom of `.gitignore` (more defensive if nested `.python-version` files ever appear — not expected here).
- Option C: drop the root `.python-version` pin entirely and rely on `pyproject.toml` `requires-python` only (loses determinism).

Recommended resolution:
Option A — remove the ignore line. Small, targeted edit within the `# Python` section. Root `.python-version` becomes trackable; no nested `.python-version` files are expected in this repo.

Operator decision:
Approved 2026-04-19 — Option A, narrow edit only, no `git add -f` usage. GAP logged in this file.

Resolution evidence:
- `.gitignore`: removed line `.python-version` between `*.pyd` and `.venv/`.
- `git check-ignore -v .python-version` now returns exit code 1 (not ignored).
- `.python-version` pinned to `3.12` per detected Python 3.12.4 interpreter.
- Will be included in Phase 1 Commit 2 (package + tooling foundation) after Gate 2 approval.

---

