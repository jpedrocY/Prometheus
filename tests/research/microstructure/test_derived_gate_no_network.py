"""Phase 4bf static no-network / no-credentials guard tests.

Scans the four ``derived_gate_*`` modules for forbidden imports and
forbidden credential / MCP / `.env` / `.mcp.json` references.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure import (
    derived_gate as dg,
)
from prometheus.research.microstructure import (
    derived_gate_checks as dgc,
)
from prometheus.research.microstructure import (
    derived_gate_io as dg_io,
)
from prometheus.research.microstructure import (
    derived_gate_report as dg_report,
)

DERIVED_GATE_MODULES = (dg_io, dgc, dg_report, dg)

FORBIDDEN_MODULE_NAMES = frozenset(
    {
        "requests",
        "httpx",
        "aiohttp",
        "urllib.request",
        "urllib3",
        "socket",
        "websockets",
        "binance",
        "dotenv",
        "python_dotenv",
    }
)

FORBIDDEN_TOKENS = frozenset(
    {
        "api_key",
        "secret",
        "signature",
        "listenKey",
        "userDataStream",
        "/fapi/v1/order",
        "/fapi/v2/account",
        "/fapi/v2/positionRisk",
        "/fapi/v1/leverage",
        "/fapi/v1/marginType",
        "/fapi/v1/forceOrders",
        ".env",
        "Graphify",
        "MCP",
        ".mcp.json",
        "os.environ",
        "getenv",
    }
)


def _strip_strings_and_comments(text: str) -> str:
    """Crude strip of triple-quoted docstrings and `#` comments."""
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


@pytest.mark.parametrize("module", DERIVED_GATE_MODULES)
def test_no_forbidden_imports(module: object) -> None:
    src_path = Path(module.__file__)  # type: ignore[arg-type]
    text = _strip_strings_and_comments(src_path.read_text(encoding="utf-8"))
    bad: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for name in FORBIDDEN_MODULE_NAMES:
            if (
                stripped.startswith(f"import {name}")
                or stripped.startswith(f"from {name} ")
                or stripped.startswith(f"from {name}.")
                or f" import {name}" in stripped
            ):
                bad.append(f"{src_path.name}:{name}")
                break
    assert not bad, f"forbidden imports found: {bad}"


@pytest.mark.parametrize("module", DERIVED_GATE_MODULES)
def test_no_forbidden_tokens(module: object) -> None:
    src_path = Path(module.__file__)  # type: ignore[arg-type]
    text = _strip_strings_and_comments(src_path.read_text(encoding="utf-8"))
    found: list[tuple[str, str]] = []
    for tok in FORBIDDEN_TOKENS:
        if tok in text:
            found.append((src_path.name, tok))
    assert not found, f"forbidden tokens found: {found}"
