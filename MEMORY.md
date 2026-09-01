# Maintainer Memory

**Last updated:** 2026-08-31

## Purpose and scope

This repository is an SDE interview-preparation study catalog with maintained
Python examples and pytest tests. Documentation is educational material; a
guide or passing example is not a production-readiness claim.

## Source of truth

- [Project specification](docs/PROJECT_SPEC.md) — repository contract and roadmap
- [CLAUDE.md](CLAUDE.md) — collaboration and content-quality conventions
- [README.md](README.md) and [docs/INDEX.md](docs/INDEX.md) — reader navigation
- [System-design status](docs/03-system-design/CONTENT_STATUS.md) and
  [AI/ML status](docs/04-ai-ml-llms/CONTENT_STATUS.md) — section boundaries
- [HANDOFF.md](HANDOFF.md) — dated worktree state, verification, and next actions

## Maintained trees and truthful status

`python/` and `tests/` are the maintained implementation/test trees; `scripts/`
contains repository gates. The six runnable systems labs consist of three
distributed-systems labs and three ML/AI labs, each with focused tests. Current
inventory is 393 passing pytest cases, 705 active system-design topic guides in
19 directories, 22 AI/ML long-form guides plus 3 ML/AI labs, and 15 domain
learning paths.

Use these labels precisely:

- **Tested:** a focused automated test exercises the educational API.
- **Reviewed:** a maintainer manually checked objective, assumptions,
  calculations, trade-offs, failure modes, and links.
- **Draft:** useful material that has not passed the reviewed standard.

## Durable decisions and conventions

- Python is the maintained implementation language and repository contract.
- Java references and old completion claims are historical unless explicitly
  re-established; do not add Java parity requirements to current tracks.
- `docs/_archive/` and the superpowers completion checklist are historical
  planning material, not current status.
- Labs are small, standard-library-only, in-memory teaching models. They omit
  production networking, persistence, coordination, security, capacity, and
  reliability concerns unless a lab explicitly says otherwise.
- Inventory counts must state what is included/excluded; do not use counts as
  completion or review claims.

## Updating this memory and the handoff

When scope, maintained trees, counts, quality gates, or decisions change, update
this file and [HANDOFF.md](HANDOFF.md) on the same documentation pass. Recount
from the checkout, record the date, run the gates below, and keep pre-existing
dirty work separate from the change being handed off.

```bash
pytest -q
python3 scripts/validate_repo.py --imports
python3 scripts/audit_system_design.py --max-structural-filler 27 --max-copied-capacity 134
git diff --check
```
