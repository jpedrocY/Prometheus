"""Static import-boundary scan for Phase 4bm-O label modules + script.

Confirms that the four new ``labels_*_v002`` source modules plus the
Phase 4bm-O generation script:

- never import any networking library;
- never reference credential-shaped tokens, ``.env`` files,
  ``.mcp.json``, or Graphify / MCP integrations in code (docstrings
  that describe the policy are allowed).

Mirrors the Phase 4bm-H ``test_features_no_network_v002.py`` pattern
(case-sensitive token scan after stripping docstrings + comments) so
that legitimate lowercase boundary-confirmation keys such as
``no_mcp_or_graphify`` are not false positives.
"""

from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PACKAGE_DIR = _REPO_ROOT / "src" / "prometheus" / "research" / "microstructure"
_SCRIPTS_DIR = _REPO_ROOT / "scripts"

_LABEL_MODULES_V002 = (
    _PACKAGE_DIR / "labels_schema_v002.py",
    _PACKAGE_DIR / "labels_io_v002.py",
    _PACKAGE_DIR / "labels_compute_v002.py",
    _PACKAGE_DIR / "labels_manifest_v002.py",
    _SCRIPTS_DIR / "phase4bm_o_compute_multiday_labels.py",
)

_FORBIDDEN_IMPORTS = (
    "requests",
    "urllib",
    "urllib.request",
    "urllib3",
    "httpx",
    "aiohttp",
    "websockets",
    "websocket",
    "binance",
    "ccxt",
    "dotenv",
    "python_dotenv",
    "socket",
)

# Case-sensitive forbidden code tokens (after stripping docstrings/comments).
# Mirrors the Phase 4bm-H test_features_no_network_v002 deny list verbatim.
_DENY_TOKENS: tuple[str, ...] = (
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
)


def _strip_docstrings_and_comments(source: str) -> str:
    """Strip module/class/function docstrings and ``#`` comments."""
    tree = ast.parse(source)

    class _DocstringStripper(ast.NodeTransformer):
        def visit_Module(self, node: ast.Module) -> ast.Module:  # type: ignore[override]
            return self._strip(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:  # type: ignore[override]
            return self._strip(node)

        def visit_AsyncFunctionDef(  # type: ignore[override]
            self, node: ast.AsyncFunctionDef
        ) -> ast.AsyncFunctionDef:
            return self._strip(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:  # type: ignore[override]
            return self._strip(node)

        def _strip(
            self,
            node: ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
        ) -> ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef:
            if node.body and isinstance(node.body[0], ast.Expr):
                first = node.body[0]
                if isinstance(first.value, ast.Constant) and isinstance(
                    first.value.value, str
                ):
                    node.body = node.body[1:]
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            return node

    stripped = ast.unparse(_DocstringStripper().visit(tree))
    tokens = tokenize.generate_tokens(io.StringIO(stripped).readline)
    filtered: list[str] = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        filtered.append(tok.string)
    return " ".join(filtered)


def _collect_imports(source: str) -> list[str]:
    tree = ast.parse(source)
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


@pytest.mark.parametrize("module_path", _LABEL_MODULES_V002)
def test_label_v002_module_has_no_forbidden_imports(module_path: Path) -> None:
    source = module_path.read_text(encoding="utf-8")
    imports = _collect_imports(source)
    flat_imports = {name.split(".")[0] for name in imports}
    flat_imports.update(imports)
    for forbidden in _FORBIDDEN_IMPORTS:
        assert forbidden not in flat_imports, (
            f"{module_path.name}: forbidden import {forbidden!r} detected"
        )


@pytest.mark.parametrize("module_path", _LABEL_MODULES_V002)
def test_label_v002_module_has_no_forbidden_code_tokens(module_path: Path) -> None:
    text = module_path.read_text(encoding="utf-8")
    code = _strip_docstrings_and_comments(text)
    for token in _DENY_TOKENS:
        assert token not in code, (
            f"{module_path.name} code (excluding docstrings/comments) must not "
            f"contain forbidden token {token!r}"
        )


@pytest.mark.parametrize("module_path", _LABEL_MODULES_V002)
def test_label_v002_module_does_not_call_os_environ(module_path: Path) -> None:
    text = module_path.read_text(encoding="utf-8")
    code = _strip_docstrings_and_comments(text)
    assert "os.environ" not in code, (
        f"{module_path.name} references os.environ"
    )
    assert "os.getenv" not in code, (
        f"{module_path.name} references os.getenv"
    )


def test_no_dot_env_or_dot_mcp_files_in_package_v002() -> None:
    for path in _PACKAGE_DIR.iterdir():
        assert path.name != ".env"
        assert path.name != ".mcp.json"


def test_label_v002_module_files_exist() -> None:
    for module_path in _LABEL_MODULES_V002:
        assert module_path.exists(), f"missing module: {module_path}"
