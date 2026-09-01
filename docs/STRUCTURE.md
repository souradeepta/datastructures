# InterviewPrep Repository Structure

This repository combines interview study material with small, runnable Python examples. The
repository root is the source of truth for navigation; `docs/` contains explanations and
`learning-paths/` contains study plans.

## Top-level map

```text
.
├── docs/                 Guides, indexes, and the project specification
│   ├── 01-interview-frameworks/
│   ├── 02-algorithms/    Category guides and algorithm notes
│   ├── 02-databases/     Database deep dives
│   ├── 03-system-design/ System-design topic catalog
│   ├── 04-ai-ml-llms/    AI/ML and LLM guides
│   ├── 05-algorithms/    Algorithm category index pages
│   ├── 06-data-structures/
│   ├── 07-patterns/      Pattern guides and problem lists
│   └── 09-senior-staff-track/
├── learning-paths/       Sequential tracks, playbooks, domains, and skill trees
├── python/               Maintained Python implementations
│   ├── algorithms/
│   ├── basic/
│   ├── patterns/
│   ├── advanced/
│   ├── advanced_ds/
│   ├── distributed_systems/  Distributed-systems teaching models
│   ├── ml_systems/        ML/AI teaching models
│   └── system_design/
├── tests/                Pytest tests for the maintained core
└── scripts/              Repository validation helpers
```

The numbering in `docs/` is historical and not a filesystem mirror of the repository. In
particular, learning paths live at the root, and implementations do not live below each guide.

## Where to start

- New to the repository: [GETTING_STARTED.md](../GETTING_STARTED.md)
- Browse all maintained entry points: [Master Index](INDEX.md)
- Choose a schedule: [Learning Paths](../learning-paths/README.md)
- Practice coding patterns: [Pattern Index](07-patterns/README.md)
- Prepare for senior/staff interviews: [Senior/Staff Track](09-senior-staff-track/README.md)
- Understand the repository contract: [Project Specification](PROJECT_SPEC.md)

## Code and test conventions

Implementations are grouped by topic under `python/`; tests are grouped under `tests/` and import
those modules directly. Run the maintained suite with:

```bash
pytest -q
python3 scripts/validate_repo.py --imports
```

The validator checks Python syntax and links in active Markdown; `--imports` also imports each
non-test implementation module. Archived material is intentionally excluded from the link gate.

## Content status

- Databases and AI/ML/LLMs contain the deepest long-form coverage.
- Frameworks and senior/staff material are curated guides.
- Algorithms, data structures, patterns, and system design combine indexes, outlines, and examples;
  coverage and example quality are still being expanded.
- `docs/_archive/` is historical and is not part of the maintained navigation contract.
