# Documentation Review Log

**Ledger rule:** append-only. Add a dated entry for a new review, correction,
or gate transition; do not rewrite or delete an earlier decision. The canonical
review standard is the [Documentation Reviewer Rubric](DOCUMENTATION_REVIEWER_RUBRIC.md).

**Current truthful state (2026-09-01):** Terra approval is recorded for Batch
1, Batch 2A, Batch 2B, and Batch 2C. Maintainer confirmation is still pending
for all four approved batches. Commit
`badde17a8e0e368391389e685e36a9da4de0b364` was pushed before Terra's final
Batch 2C verdict; corrected pushed-state records were confirmed and PASSed in
`a6cea95f071802f41f6b11b6afee5e6763c364ac`. The remaining three Batch 2
guides and Batches 3–5 remain open planning cohorts.

## Existing approval records

These entries preserve and link the detailed per-guide records already recorded
in the [upgrade plan](DOCUMENTATION_UPGRADE_PLAN.md):

| Entry | Cohort | Terra decision | Date | Maintainer confirmation | Detailed record |
| --- | --- | --- | --- | --- | --- |
| `2026-08-31-batch-1` | Batch 1 — database foundations (8 guides) | PASS — approved after review and corrections | 2026-08-31 | Pending | [Batch 1 gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-1--database-foundations-this-change) |
| `2026-09-01-batch-2a` | Batch 2A — database operations and scale (8 guides) | PASS — final gate approved | 2026-09-01 | Pending | [Batch 2A gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-2a--database-operations-and-scale-approved) |
| `2026-09-01-batch-2b` | Batch 2B — analytical data paths and tenant boundaries (8 guides) | PASS — final gate approved | 2026-09-01 | Pending | [Batch 2B gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-2b--analytical-data-paths-and-tenant-boundaries-approved) |
| `2026-09-01-batch-2c` | Batch 2C — distributed correctness and runtime evidence (3 guides) | PASS — corrected pushed-state records and final gate approved | 2026-09-01 | Pending | [Batch 2C gate and sign-offs](DOCUMENTATION_UPGRADE_PLAN.md#batch-2c--distributed-correctness-and-runtime-evidence-reviewedapproved) |

The linked plan sections contain the exact paths and per-guide reviewer rows.
No path outside those records is approved by this ledger.

## Maintainer confirmation queue

- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 1 guides.
- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 2A guides.
- [ ] Confirm the recorded `reviewed`/`approved` metadata for all Batch 2B guides.
- [ ] Decide ownership and entry criteria before opening a future cohort.

## Open future cohorts

The profile registry lists exact planning paths for the remaining three Batch 2
guides, Batch 3A, Batch 4A, and selected Batch 5 system-design cohorts. The
remaining cohorts remain `open` and non-enforced.

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
  Batch 2B records are unchanged. This checkpoint predates the later
  push-first workflow event.

### 2026-09-01 — Batch 2C pushed-state Terra review

- At the user's explicit request, commit
  `badde17a8e0e368391389e685e36a9da4de0b364` was pushed before Terra's final
  verdict.
- Terra reviewed the pushed state and confirmed the Batch 2C content and
  structural gates. The review failed only because the handoff, memory, plan,
  and ledger records were stale/inconsistent about the push-first state.
- Batch 2C remains `Status: draft` with `Terra gate: open`; no approval or
  reviewed sign-off is recorded. Next gate: correct and reverify the records,
  then obtain Terra's follow-up confirmation. Any content corrections remain
  follow-up work and must preserve draft/open status until a passing gate.

### 2026-09-01 — Batch 2C corrected pushed-state Terra PASS — consensus algorithms

- Terra confirmed the corrected pushed-state records in commit
  `a6cea95f071802f41f6b11b6afee5e6763c364ac` and PASSed the content and
  structural gates for `docs/02-databases/13-consensus-algorithms.md`.

### 2026-09-01 — Batch 2C corrected pushed-state Terra PASS — distributed tracing

- Terra confirmed the corrected pushed-state records in commit
  `a6cea95f071802f41f6b11b6afee5e6763c364ac` and PASSed the content and
  structural gates for `docs/02-databases/22-distributed-tracing.md`.

### 2026-09-01 — Batch 2C corrected pushed-state Terra PASS — stream processing

- Terra confirmed the corrected pushed-state records in commit
  `a6cea95f071802f41f6b11b6afee5e6763c364ac` and PASSed the content and
  structural gates for `docs/02-databases/30-stream-processing.md`.
