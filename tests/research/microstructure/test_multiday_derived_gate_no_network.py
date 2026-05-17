"""Phase 4bm-D static no-network / no-credential scan.

Asserts that the four multi-day derived-gate modules (orchestrator,
I/O, checks, report) carry zero imports of any network or
credential-handling package, and zero substring references to any
credential-shaped token, after stripping module/function/class
docstrings and ``#`` comments (which legitimately describe the
boundary discipline). Source-level guarantee that the gate cannot
perform network I/O, cannot read credentials, and cannot read
``.env`` files.

Mirrors the Phase 4bf ``test_derived_gate_no_network.py`` pattern.
"""
from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MODULE_DIR = _REPO_ROOT / "src" / "prometheus" / "research" / "microstructure"
_TARGET_MODULES: tuple[Path, ...] = (
    _MODULE_DIR / "multiday_derived_gate.py",
    _MODULE_DIR / "multiday_derived_gate_io.py",
    _MODULE_DIR / "multiday_derived_gate_checks.py",
    _MODULE_DIR / "multiday_derived_gate_report.py",
)

# Top-level package names the multi-day gate is forbidden from
# importing in any form (``import X``, ``import X.sub``, ``from X
# import Y``, ``from X.sub import Y``).
_FORBIDDEN_IMPORT_ROOTS: frozenset[str] = frozenset(
    {
        "requests",
        "httpx",
        "aiohttp",
        "urllib",
        "urllib3",
        "socket",
        "websockets",
        "binance",
        "dotenv",
        "python_dotenv",
    }
)

# Credential-shaped tokens checked as plain substrings against code
# (docstrings and comments stripped first).
_FORBIDDEN_TOKENS: tuple[str, ...] = (
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "API_KEY",
    "API_SECRET",
    "SECRET_KEY",
    "PRIVATE_KEY",
    "LISTEN_KEY",
    "listenKey",
    ".env",
    "dotenv",
)


def _strip_strings_and_comments(text: str) -> str:
    """Strip triple-quoted docstrings and ``#`` comments.

    Crude line-oriented pass matching the Phase 4bf
    ``test_derived_gate_no_network`` helper exactly; sufficient for
    these modules, which only use triple-quoted docstrings at the
    module / class / function level.
    """
    out_lines: list[str] = []
    in_docstring = False
    docstring_quote: str | None = None
    for raw_line in text.splitlines():
        line = raw_line
        if in_docstring:
            assert docstring_quote is not None
            if docstring_quote in line:
                in_docstring = False
                docstring_quote = None
            continue
        for q in ('"""', "'''"):
            if q in line and line.count(q) % 2 == 1:
                in_docstring = True
                docstring_quote = q
                line = line.split(q, 1)[0]
                break
        if "#" in line:
            line = line.split("#", 1)[0]
        out_lines.append(line)
    return "\n".join(out_lines)


def test_target_modules_exist() -> None:
    for p in _TARGET_MODULES:
        assert p.is_file(), f"missing target module: {p}"


@pytest.mark.parametrize(
    "module_path", _TARGET_MODULES, ids=lambda p: p.name
)
def test_no_forbidden_imports(module_path: Path) -> None:
    text = _strip_strings_and_comments(
        module_path.read_text(encoding="utf-8")
    )
    bad: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for name in _FORBIDDEN_IMPORT_ROOTS:
            if (
                stripped.startswith(f"import {name}")
                or stripped.startswith(f"from {name} ")
                or stripped.startswith(f"from {name}.")
                or f" import {name}" in stripped
            ):
                bad.append(f"{module_path.name}:{name}")
                break
    assert not bad, f"forbidden imports found: {bad}"


@pytest.mark.parametrize(
    "module_path", _TARGET_MODULES, ids=lambda p: p.name
)
def test_no_forbidden_tokens(module_path: Path) -> None:
    text = _strip_strings_and_comments(
        module_path.read_text(encoding="utf-8")
    )
    found = [tok for tok in _FORBIDDEN_TOKENS if tok in text]
    assert not found, (
        f"{module_path.name} contains forbidden credential-shaped tokens "
        f"in non-comment / non-docstring code: {sorted(set(found))}"
    )
