#!/usr/bin/env python3
"""Audit known content debt in the active system-design catalog.

The audit checks two measurable debt signatures. It reports existing debt so
maintainers can track it, while CI fails only when either count exceeds its
approved baseline.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path


STRUCTURAL_FILLER_MARKERS = ("Primary element", "Advantage 1", "Use case 1")
COPIED_CAPACITY_MARKERS = (
    "Total daily requests = 100M users",
    "474 MB/s",
)


def active_guides(root: Path) -> list[Path]:
    """Return active system-design guides, excluding landing pages."""
    catalog = root / "docs" / "03-system-design"
    return sorted(
        path
        for path in catalog.rglob("*.md")
        if "_archive" not in path.relative_to(root).parts
        and path.name != "README.md"
        and len(path.relative_to(catalog).parts) > 1
    )


def matching_guides(root: Path) -> tuple[list[Path], list[Path]]:
    """Find structural-filler and copied-capacity guides."""
    filler = []
    capacity = []
    for path in active_guides(root):
        content = path.read_text(encoding="utf-8")
        if all(marker in content for marker in STRUCTURAL_FILLER_MARKERS):
            filler.append(path)
        if all(marker in content for marker in COPIED_CAPACITY_MARKERS):
            capacity.append(path)
    return filler, capacity


def grouped_paths(paths: list[Path], root: Path) -> dict[str, list[str]]:
    """Group paths by their first system-design category directory."""
    groups: dict[str, list[str]] = defaultdict(list)
    catalog = root / "docs" / "03-system-design"
    for path in paths:
        relative = path.relative_to(catalog)
        category = relative.parts[0] if len(relative.parts) > 1 else "."
        groups[category].append(str(path.relative_to(root)))
    return dict(sorted(groups.items()))


def print_grouped(label: str, paths: list[Path], root: Path) -> None:
    print(f"{label}: {len(paths)}")
    for category, entries in grouped_paths(paths, root).items():
        print(f"  {category} ({len(entries)}):")
        for entry in entries:
            print(f"    - {entry}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--max-structural-filler",
        type=int,
        default=27,
        help="Approved maximum number of structural-filler guides (default: 27)",
    )
    parser.add_argument(
        "--max-copied-capacity",
        type=int,
        default=134,
        help="Approved maximum number of copied-capacity guides (default: 134)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    filler, capacity = matching_guides(root)

    print("System-design content audit")
    print_grouped("Structural filler guides", filler, root)
    print_grouped("Copied-capacity guides", capacity, root)
    print(
        "Thresholds: "
        f"structural filler <= {args.max_structural_filler}, "
        f"copied capacity <= {args.max_copied_capacity}"
    )

    exceeded = []
    if len(filler) > args.max_structural_filler:
        exceeded.append(
            f"structural filler {len(filler)} > {args.max_structural_filler}"
        )
    if len(capacity) > args.max_copied_capacity:
        exceeded.append(
            f"copied capacity {len(capacity)} > {args.max_copied_capacity}"
        )
    if exceeded:
        print("Audit failed: " + "; ".join(exceeded), file=sys.stderr)
        return 1

    print("Audit passed: no content-debt threshold exceeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
