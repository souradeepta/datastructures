# Documentation Review Log

**Ledger rule:** append-only. Add a dated entry for a new review, correction,
or gate transition; do not rewrite or delete an earlier decision. The canonical
review standard is the [Documentation Reviewer Rubric](DOCUMENTATION_REVIEWER_RUBRIC.md).

**Current truthful state (2026-09-01):** Terra approval is recorded for Batch
1, Batch 2A, and Batch 2B. Maintainer confirmation is still pending for all
three batches. Batch 2C, Batch 3A, Batch 4A, and Batch 5 are open planning
cohorts; no future cohort approval is claimed.

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
4A, and selected Batch 5 system-design cohorts. They remain `open` and
non-enforced. The three remaining Batch 2 guides are not upgraded in this
review-system pass.

## Append-only entries

### 2026-09-01 — reviewer-system foundation

- Added the canonical rubric and central profile registry.
- Preserved the three existing Terra-approved cohort decisions above.
- Maintainer confirmation: **pending**.
- Future cohorts: **open**, with no Terra approval or repository-wide review
  claim.
