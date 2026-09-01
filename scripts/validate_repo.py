#!/usr/bin/env python3
"""Validate Python syntax and links in active Markdown documentation."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
EXCLUDED_DIRS = {".git", ".claude", "docs/00-resources", "docs/superpowers"}


def is_excluded(path: Path, root: Path) -> bool:
    relative = str(path.relative_to(root))
    return any(
        relative == excluded or relative.startswith(f"{excluded}/")
        for excluded in EXCLUDED_DIRS
    ) or "_archive" in path.relative_to(root).parts


def without_code_blocks(content: str) -> str:
    """Avoid treating examples in fenced code blocks as live links."""
    return re.sub(r"```.*?```", "", content, flags=re.DOTALL)


def python_errors(root: Path) -> list[str]:
    errors = []
    for path in sorted((root / "python").rglob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    return errors


def import_errors(root: Path) -> list[str]:
    """Import implementation modules without running their CLI examples."""
    errors = []
    for path in sorted((root / "python").rglob("*.py")):
        if path.name.startswith("test_") or path.name == "__init__.py":
            continue
        module_name = "_repo_validate_" + "_".join(path.relative_to(root).with_suffix("").parts)
        try:
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise ImportError("could not create an import specification")
            module = importlib.util.module_from_spec(spec)
            # Some standard-library decorators (notably dataclasses) resolve
            # the defining module through sys.modules while it is executing.
            # Mirror normal import behavior before running the module.
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        except Exception as exc:  # modules are educational examples; report their failure
            errors.append(f"{path.relative_to(root)}: {exc}")
    return errors


def link_target(raw_target: str) -> str:
    target = raw_target.strip().split(None, 1)[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def markdown_errors(root: Path) -> list[str]:
    errors = []
    markdown_files = sorted(
        path
        for path in root.rglob("*.md")
        if not is_excluded(path, root)
    )
    for source in markdown_files:
        try:
            content = source.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{source.relative_to(root)}: {exc}")
            continue
        for match in LINK_RE.finditer(without_code_blocks(content)):
            target = link_target(match.group(1))
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//") or target.startswith("#"):
                continue
            path_text = unquote(parsed.path)
            resolved = (source.parent / path_text).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(
                    f"{source.relative_to(root)}: link escapes repository: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(f"{source.relative_to(root)}: missing link target: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--python-only", action="store_true", help="Skip active Markdown link checks"
    )
    parser.add_argument(
        "--links-only", action="store_true", help="Skip Python syntax checks"
    )
    parser.add_argument(
        "--imports", action="store_true", help="Also import non-test Python modules"
    )
    args = parser.parse_args()
    root = args.root.resolve()

    errors = []
    if not args.links_only:
        errors.extend(python_errors(root))
        if args.imports:
            errors.extend(import_errors(root))
    if not args.python_only:
        errors.extend(markdown_errors(root))

    if errors:
        print("Repository validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    checks = []
    if not args.links_only:
        checks.append("Python syntax")
    if not args.python_only:
        checks.append("active Markdown links")
    print(f"Passed: {' and '.join(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
