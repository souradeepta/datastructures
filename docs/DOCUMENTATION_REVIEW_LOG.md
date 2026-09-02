# Documentation Review Log

**Ledger rule:** append-only. Add a dated entry for a new review, correction,
or gate transition; do not rewrite or delete an earlier decision. The canonical
review standard is the [Documentation Reviewer Rubric](DOCUMENTATION_REVIEWER_RUBRIC.md).

**Current truthful state (2026-09-01):** Terra approval is recorded for Batch
1, Batch 2A, and Batch 2B. Maintainer confirmation is still pending for all
three approved batches. Batch 2C is implemented as three `draft`/`open` guides
with a strict local profile, but Terra review and maintainer confirmation are
pending; no Batch 2C approval is claimed. Batch 3A, Batch 4A, and Batch 5
remain open planning cohorts.

## Existing approval records

These entries preserve and link the detailed per-guide records already recorded
in the [upgrade plan](DOCUMENTATION_UPGRADE_PLAN.md):

| Entry | Cohort | Terra decision | Date | Maintainer confirmation | Detailed record |
| --- | --- | --- | --- | --- | --- |
| `2026-08-31-batch-1` | Batch 1 — database foundations (8 guides) | PASS — approved after review and corrections | 2026-08-31 | Pending | [Batch 1 gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-1--database-foundations-this-change) |
| `2026-09-01-batch-2a` | Batch 2A — database operations and scale (8 guides) | PASS — final gate approved | 2026-09-01 | Pending | [Batch 2A gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-2a--database-operations-and-scale-approved) |
| `2026-09-01-batch-2b` | Batch 2B — analytical data paths and tenant boundaries (8 guides) | PASS — final gate approved | 2026-09-01 | Pending | [Batch 2B gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-2b--analytical-data-paths-and-tenant-boundaries-approved) |

The linked plan sections contain the exact paths and per-guide reviewer rows.
No path outside those records is approved by this ledger.

## Maintainer confirmation queue

- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 1 guides.
- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 2A guides.
- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 2B guides.
- [ ] Decide ownership and entry criteria before opening a future cohort.

## Open future cohorts

The profile registry lists exact planning paths for Batch 2C, Batch 3A, Batch
4A, and selected Batch 5 system-design cohorts. Batch 2C is `open` and locally
strict, but non-enforced in CI until Terra review. The later cohorts remain
`open` and non-enforced.

## Append-only entries

### 2026-09-01 — reviewer-system foundation

- Added the canonical rubric and central profile registry.
- Preserved the three existing Terra-approved cohort decisions above.
- Maintainer confirmation: **pending**.
- Future cohorts: **open**, with no Terra approval or repository-wide review
  claim.

### 2026-09-01 — Batch 2C implementation checkpoint

- Implemented the three ordered Batch 2C guides as `Status: draft` with
  `Terra gate: open`.
- Added strict local profile validation for the exact paths, ranges, required
  terms, diagrams, tables, exercises, Q&A, and local links.
- Terra review and maintainer confirmation: **pending**. The profile remains
  outside CI enforcement; no approval is claimed.

### 2026-09-01 — Batch 2C correction checkpoint

- Corrected the distributed-tracing single-message path to use the producer's
  remote parent; span links and new roots are reserved for intentional
  detachment such as replay, fan-in, and batch work.
- Made the fraud worked example and exercise explicitly use the aligned,
  non-overlapping tumbling `[12:00, 12:10)` window while preserving stable
  business/window identity, revision ordering, and late-data reconciliation.
- Made underscore a word character for bounded topic terms and added negative
  regression coverage for underscore identifiers while retaining `2f+1` and
  `parent/child` matches.
- Verification: `pytest -q` **456 passed**; validation, Batch 1/2A/2B, and
  local Batch 2C profiles passed; summary remained 1,003 active Markdown files
  with diagnostics 250/277/684/280; system audit remained 27/134; diff check
  passed. Batch 2C remains `draft`/`open`; approved Batch 1, Batch 2A, and
  Batch 2B records are unchanged. No commit or push was made.
