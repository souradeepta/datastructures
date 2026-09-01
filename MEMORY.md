# Maintainer Memory

**Last updated:** 2026-09-01

## Current documentation upgrade pass

Terra is the curriculum architect and final gate for the repository-wide
documentation upgrade. The versioned [upgrade plan](docs/DOCUMENTATION_UPGRADE_PLAN.md)
defines the active-file boundary, guide contract, sequence, depth targets,
technical accuracy checks, and sign-off fields. The first implementation batch
covers these eight database guides:

- `docs/02-databases/01-sql-advanced.md`
- `docs/02-databases/02-nosql-advanced.md`
- `docs/02-databases/03-graph-databases.md`
- `docs/02-databases/08-vector-databases.md`
- `docs/02-databases/12-distributed-transactions.md`
- `docs/02-databases/15-database-replication.md`
- `docs/02-databases/18-indexing-deep-dive.md`
- `docs/02-databases/20-change-data-capture.md`

Batch 1 is Terra-approved: all eight guides are `reviewed` with `Terra gate:
approved` after corrections. Maintainer confirmation remains explicit. Remaining
batches are the rest of the database catalog, AI/ML, learning paths/interview
frameworks, and the system-design catalog. The
standard-library scanner is `scripts/audit_documentation.py`, with focused tests
in `tests/test_documentation_audit.py`.

Batch 2A is Terra-approved after the final gate passed on 2026-09-01. Its eight
guides are recorded as `reviewed` with `Terra gate: approved`, in this order:

- `docs/02-databases/17-query-planning.md`
- `docs/02-databases/25-connection-pooling.md`
- `docs/02-databases/24-database-monitoring.md`
- `docs/02-databases/16-backup-recovery.md`
- `docs/02-databases/21-eventual-consistency.md`
- `docs/02-databases/19-sharding-advanced.md`
- `docs/02-databases/26-migration-strategies.md`
- `docs/02-databases/28-database-security.md`

The strict profile is `python3 scripts/audit_documentation.py --profile
batch-2a --fail-on-missing --summary`, and its structural gate passes. Terra's
Batch 2A final gate is approved; maintainer confirmation and the broader
Batches 2–5 remain open.

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
verified state is 414 passing pytest cases, 705 active system-design topic guides in
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
- Batch 1 and Batch 2A are Terra-approved; maintainer confirmation remains open.
  The broader Batches 2–5 remain open.

## Verified documentation gates

The documentation audit summary reports 1,001 active Markdown files, with
repository-wide diagnostics of 259 files without Mermaid, 276 without Q&A, 689
without a trade-off table, and 289 without a What/Why signal. These diagnostics
are not Batch-1 failures. The strict `batch-1 --fail-on-missing` profile passes
with all eight required paths present and checks per-exercise guidance plus an
Answer and Follow-up for every Q&A block. All eight Batch 1 per-guide Terra rows
are recorded as PASS on 2026-08-31, and all eight Batch 2A rows are recorded as
PASS on 2026-09-01. Repository-wide diagnostics remain visible and are not
claims that all 1,001 active files are upgraded.

The recorded gates are: `pytest -q` → 414 passed; `python3
scripts/validate_repo.py --imports` → passed; both documentation audit commands
→ passed; `python3 scripts/audit_system_design.py --max-structural-filler 27
--max-copied-capacity 134` → passed at 27/134; and `git diff --check` → passed
with no output. The strict Batch 2A profile also passes for all eight
reviewed/approved guides.

## Updating this memory and the handoff

When scope, maintained trees, counts, quality gates, or decisions change, update
this file and [HANDOFF.md](HANDOFF.md) on the same documentation pass. Recount
from the checkout, record the date, run the gates below, and keep pre-existing
dirty work separate from the change being handed off.

```bash
pytest -q
python3 scripts/validate_repo.py --imports
python3 scripts/audit_system_design.py --max-structural-filler 27 --max-copied-capacity 134
python3 scripts/audit_documentation.py --summary
python3 scripts/audit_documentation.py --profile batch-1 --fail-on-missing --summary
python3 scripts/audit_documentation.py --profile batch-2a --fail-on-missing --summary
git diff --check
```
