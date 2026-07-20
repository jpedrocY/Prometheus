"""Phase 4bn-AZ — static no-network / no-credentials / no-reserve guard for CF-1 code.

Scans the three CF-1 source modules and the orchestration script for forbidden imports
(networking / exchange / dotenv) and forbidden credential / MCP / ``.env`` / endpoint
tokens, and asserts the runtime governance / non-authorization flags are all false.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure import cf1_artifacts_v001 as art
from prometheus.research.microstructure import cf1_evaluation_v001 as ev
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1

_REPO_ROOT = Path(cf1.__file__).resolve().parents[4]
_SCRIPT = _REPO_ROOT / "scripts" / "phase4bn_az_cf1_realized_volatility_execution.py"

CF1_FILES = (
    Path(cf1.__file__),
    Path(ev.__file__),
    Path(art.__file__),
    _SCRIPT,
)

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
        ".env",
        "Graphify",
        ".mcp.json",
        "os.environ",
        "getenv",
    }
)


def _strip_strings_and_comments(text: str) -> str:
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


@pytest.mark.parametrize("path", CF1_FILES, ids=lambda p: p.name)
def test_no_forbidden_imports(path: Path) -> None:
    text = _strip_strings_and_comments(path.read_text(encoding="utf-8"))
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
                bad.append(f"{path.name}:{name}")
                break
    assert not bad, f"forbidden imports: {bad}"


@pytest.mark.parametrize("path", CF1_FILES, ids=lambda p: p.name)
def test_no_forbidden_tokens(path: Path) -> None:
    text = _strip_strings_and_comments(path.read_text(encoding="utf-8"))
    found = [tok for tok in FORBIDDEN_TOKENS if tok in text]
    assert not found, f"forbidden tokens in {path.name}: {found}"


def test_script_file_exists() -> None:
    assert _SCRIPT.is_file()


def test_non_authorization_flags_all_false() -> None:
    assert all(v is False for v in art.NON_AUTHORIZATION_FLAGS.values())


def test_governance_flags_reserves_untouched() -> None:
    g = art.GOVERNANCE_FLAGS
    assert g["v002_terminal_window_read"] is False
    assert g["sealed_test_split_touched"] is False
    assert g["test_rows_loaded"] == 0
    assert g["november_buffer_opened"] is False
    assert g["consumed_holdout_opened"] is False
    assert g["network_used"] is False
    assert g["data_acquisition_used"] is False
