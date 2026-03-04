from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend" / "itsor"
ALLOWLIST_FILE = Path(__file__).with_name("architecture_import_allowlist.txt")


def _iter_python_files(root: Path):
    for file_path in root.rglob("*.py"):
        if "__pycache__" in file_path.parts:
            continue
        yield file_path


def _extract_imports(file_path: Path) -> list[tuple[int, str]]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module:
                imports.append((node.lineno, module))

    return imports


def _find_violations() -> set[tuple[str, str, str]]:
    violations: set[tuple[str, str, str]] = set()

    api_root = BACKEND_ROOT / "api"
    domain_root = BACKEND_ROOT / "domain"

    for file_path in _iter_python_files(api_root):
        rel = file_path.relative_to(REPO_ROOT).as_posix()
        for _, imported in _extract_imports(file_path):
            if imported.startswith("itsor.domain"):
                violations.add(("api_to_domain", rel, imported))
            if imported.startswith("itsor.infrastructure"):
                violations.add(("api_to_infrastructure", rel, imported))

    for file_path in _iter_python_files(domain_root):
        rel = file_path.relative_to(REPO_ROOT).as_posix()
        for _, imported in _extract_imports(file_path):
            if imported.startswith("itsor.api"):
                violations.add(("domain_to_api", rel, imported))
            if imported.startswith("itsor.infrastructure"):
                violations.add(("domain_to_infrastructure", rel, imported))

    return violations


def _load_allowlist() -> set[tuple[str, str, str]]:
    if not ALLOWLIST_FILE.exists():
        return set()

    allowed: set[tuple[str, str, str]] = set()
    for raw in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        rule, rel_path, imported = [part.strip() for part in line.split("|", maxsplit=2)]
        allowed.add((rule, rel_path, imported))
    return allowed


def test_architecture_import_boundaries() -> None:
    violations = _find_violations()
    allowlist = _load_allowlist()

    new_violations = sorted(violations - allowlist)
    stale_allowlist = sorted(allowlist - violations)

    if not new_violations and not stale_allowlist:
        return

    messages: list[str] = ["Architecture import boundary violations detected."]
    if new_violations:
        messages.append("New violations:")
        messages.extend(f"  - {rule} | {rel_path} | {imported}" for rule, rel_path, imported in new_violations)
    if stale_allowlist:
        messages.append("Stale allowlist entries (safe to remove):")
        messages.extend(f"  - {rule} | {rel_path} | {imported}" for rule, rel_path, imported in stale_allowlist)

    raise AssertionError("\n".join(messages))
