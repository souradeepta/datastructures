# Repository Documentation Upgrade Plan

**Version:** 1.5
**Date:** 2026-09-01
**Owner:** repository maintainers

## Reviewer system

The canonical human-review standard is the
[Documentation Reviewer Rubric](DOCUMENTATION_REVIEWER_RUBRIC.md). Dated Terra
decisions and the still-pending maintainer confirmation are preserved in the
[append-only Documentation Review Log](DOCUMENTATION_REVIEW_LOG.md). The
machine-readable cohort registry is
[`scripts/documentation_profile_definitions.py`](../scripts/documentation_profile_definitions.py);
the audit is structural evidence only.

## Terra review gate and tracked TODO

Batch 1 is Terra-approved after review and corrections. The repository-wide
documentation upgrade remains in progress; the maintainer must still confirm
the recorded status and broader-batch work remains open.

- [x] Terra review: SQL semantics, planner claims, and isolation examples.
- [x] Terra review: NoSQL partition-key, conditional-write, and consistency claims.
- [x] Terra review: graph traversal bounds, authorization freshness, and path examples.
- [x] Terra review: vector metric/index claims, filtered recall, and model versioning.
- [x] Terra review: distributed transaction failure/retry and compensation semantics.
- [x] Terra review: replication quorum, failover, lag, and RPO/RTO claims.
- [x] Terra review: index access paths, statistics, and write-amplification claims.
- [x] Terra review: CDC offsets, snapshots, ordering, duplicates, and schema evolution.
- [ ] Maintainer records reviewed status and closes this gate only after all checks pass.

Remaining work is maintainer confirmation, provider/version-specific verification
where a product is named, and the uneven repository-wide catalog in Batches 3–5.

## Verified baseline

Terra's inventory was rechecked on 2026-08-31 before this upgrade. It counted
**1,000 active Markdown files**: Markdown under `docs/` and `learning-paths/`,
excluding `_archive/`, the six historical planning files under
`docs/00-resources/` and `docs/superpowers/`, and no generated cache content.
The new plan itself is active content, and the reviewer rubric and log are also
active content; the audit run after this change is expected to report 1,003
active files.

Terra's section metrics at that baseline were:

| Area | Baseline metric | Boundary |
| --- | ---: | --- |
| Interview frameworks | 60 guides | `docs/01-interview-frameworks/` |
| Databases | 30 long-form guides | `docs/02-databases/` (landing page and question bank excluded) |
| System design | 705 topic guides in 19 directories | `docs/03-system-design/` (landing/status/README pages excluded) |
| AI/ML/LLMs | 22 long-form guides | `docs/04-ai-ml-llms/` (landing/status pages excluded) |
| Domain learning paths | 15 paths | `learning-paths/domains/` |
| Coding patterns | 5 libraries | `docs/07-patterns/` |
| Topic sections | 7 | the numbered `docs/` study sections represented in the repository index |

These are inventory measures, not claims that every file is reviewed or
production-ready. The repeatable inventory boundary is implemented in
`scripts/audit_documentation.py`.

## Definitions

- **Active file:** a UTF-8 `*.md` file below `docs/` or `learning-paths/` that
  is not in `_archive/`, `docs/00-resources/`, or `docs/superpowers/`. Active
  includes landing pages and indexes so navigation debt remains visible; the
  report separately labels those files.
- **Topical guide:** an active Markdown file that teaches one bounded topic,
  rather than primarily linking to other files. A guide normally has an
  explanatory body, examples, and an exercise or interview practice.
- **Navigation/index:** a README, INDEX, table of contents, status page, or
  other file whose primary purpose is routing readers. Navigation is active but
  is not counted as a topical guide in section metrics.
- **Learning path:** an ordered sequence of study topics, exercises, or review
  checkpoints under `learning-paths/`; a domain path is a reusable topic path,
  while a sequential track or interview playbook is a time/stage path.
- **Tested:** an implementation or exercise has a focused automated test in
  `tests/`, or the guide's documented verification command has been run and
  recorded. Tested examples are educational contracts, not production claims.
- **Reviewed:** a maintainer has manually checked scope, terminology,
  calculations, trade-offs, failure modes, exercises, and links against the
  guide template.
- **Draft:** useful content that has not passed the reviewed standard. Draft
  content must not imply that its capacity numbers or architecture are
  production guidance.

## Reusable guide template

Every upgraded topical guide should use explicit headings in this order (small
topic-specific additions are welcome):

1. `What it is` — define the mechanism and its boundary.
2. `Why it exists / Why it matters` — identify the workload or failure it addresses.
3. `Mental model` — explain state, control flow, invariants, and what changes on failure.
4. `Worked example` — state realistic assumptions, show the calculation or trace,
   and qualify estimates instead of presenting universal latency/throughput claims.
5. `Advantages and limitations` — include a comparison table with meaningful
   alternatives and explicit consistency, cost, latency, operational, and scale trade-offs.
6. `Topic-specific visual` — include at least one Mermaid diagram and explain how
   to read it immediately below or beside the diagram.
7. `Failure modes and operations` — cover detection, recovery, idempotency,
   observability, rollout, and data-loss or staleness implications.
8. `Practical exercises` — give a solution, pseudocode, or an objectively
   checkable expected approach.
9. `Interview questions` — provide at least six questions. Each answer must
   include a follow-up or probing angle, not just a one-line definition.

### Per-guide contract and metadata

Each guide begins with a metadata block containing `Level`, `Status`,
`Prerequisites`, and (when the guide is in a planned batch) its sequence number.
The body must state 3–6 measurable learning objectives and the intended audience
(for example, “engineer preparing for an L4–L5 system design interview” or
“operator debugging a production read path”). Depth targets are **at least 350
lines for a foundational guide**, **at least 250 lines for a focused guide**,
and enough worked detail that a reader can reproduce the exercise without
guessing omitted assumptions. Line count is a floor, not permission to pad.

The acceptance record for each guide is:

| Field | Required value |
| --- | --- |
| `Guide status` | `draft`, `reviewed`, or `tested`; never imply `reviewed` from a passing parser |
| `Terra gate` | `open` until Terra curriculum review; then `approved` or `corrections-required` |
| Audience/prerequisites | Explicit paragraph and metadata fields |
| Learning objectives | 3–6 observable objectives |
| Sequence | Batch and reading order/links stated where dependencies exist |
| Core depth | What/why, mental model, realistic worked example, failure/operations |
| Comparisons | At least one Markdown table with 2+ alternatives and concrete trade-offs |
| Visuals | At least one valid Mermaid diagram with topic-specific explanatory prose |
| Practice | At least 3 exercises; each has a solution or checkable expected approach |
| Interview practice | At least 6 Q&A entries; every answer has a follow-up |
| Accuracy review | Units, complexity qualifiers, consistency scope, version/provider caveats, and links checked |
| Terra sign-off | Reviewer, date, decision, corrections, and follow-up issue/path recorded |

The sign-off record may live in this plan for the first batch or in a linked
review log, but it must be explicit. The final first-batch record is:

| Guide | Guide status | Terra gate | Reviewer | Date | Decision/corrections | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/02-databases/01-sql-advanced.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/02-nosql-advanced.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/03-graph-databases.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/08-vector-databases.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/12-distributed-transactions.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/15-database-replication.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/18-indexing-deep-dive.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |
| `docs/02-databases/20-change-data-capture.md` | `reviewed` | `approved` | Terra | 2026-08-31 | PASS — no blocking/major issues remained after corrections | Maintainer confirmation |

### Sequence and depth targets

Read Batch 1 in this order: SQL foundations (`01`), NoSQL access-pattern
contrast (`02`), graph traversal (`03`), vector retrieval (`08`), distributed
transaction boundaries (`12`), replication/failover (`15`), indexing mechanics
(`18`), and CDC/replay (`20`). The sequence moves from local query semantics to
distributed data movement. A guide can link forward, but must explain any
prerequisite instead of assuming the reader knows it.

Foundational guides target 350–600 substantive lines, two or more comparison
tables when the topic has multiple protocols, one or more diagrams per major
mechanism, four or more practical exercises, and 8–12 interview Q&A entries.
Focused guides may target 250–450 lines, one comparison table, three exercises,
and six to eight Q&A entries. All eight first-batch guides are foundational for
this plan; Terra may require more depth after review.

### Mermaid acceptance rules

- Use a fenced `mermaid` block with valid Mermaid syntax and stable, descriptive IDs.
- The visual must represent the guide's actual topic: data flow, state machine,
  query plan, transaction protocol, index layout, replication timeline, or
  another concrete mechanism.
- Label important edges with events, guarantees, or failure behavior. Keep a
  diagram readable in a narrow rendered page.
- Add explanatory prose that names the invariant or trade-off the reader should
  notice; a diagram without interpretation does not satisfy the template.
- Do not copy one generic client/server diagram into unrelated guides. **Diagrams
  must be topic-specific, not generic placeholders.**

## Prioritized batches

### Batch 1 — database foundations (this change)

| Exact path | Rationale |
| --- | --- |
| `docs/02-databases/01-sql-advanced.md` | Establishes query semantics, planner reasoning, and measurable SQL examples. |
| `docs/02-databases/02-nosql-advanced.md` | Connects access-pattern-first modeling to consistency and partition behavior. |
| `docs/02-databases/03-graph-databases.md` | Makes traversal cost, modeling, and high-degree failure modes concrete. |
| `docs/02-databases/08-vector-databases.md` | Separates embedding quality from ANN index behavior and retrieval evaluation. |
| `docs/02-databases/12-distributed-transactions.md` | Teaches the correctness boundary between 2PC, sagas, and local transactions. |
| `docs/02-databases/15-database-replication.md` | Grounds failover, lag, RPO/RTO, and split-brain reasoning in replication mechanics. |
| `docs/02-databases/18-indexing-deep-dive.md` | Replaces blanket index claims with access paths, selectivity, and write cost. |
| `docs/02-databases/20-change-data-capture.md` | Covers offsets, snapshots, ordering, duplicate delivery, and schema evolution. |

Update `docs/02-databases/README.md` only for useful links to this plan and the
audit command. Keep the catalog readable; do not turn it into a second status
database.

### Batch 2 — remaining database guide families

Prioritize `docs/02-databases/04-columnar-databases.md`,
`05-timeseries-databases.md`, `06-search-engines.md`, `07-caching-stores.md`,
`10-warehousing-lakehouses.md`, `11-message-queues-streams.md`,
`13-consensus-algorithms.md`, `16-backup-recovery.md`, `17-query-planning.md`,
`19-sharding-advanced.md`, `21-eventual-consistency.md`,
`22-distributed-tracing.md`, `24-database-monitoring.md`,
`25-connection-pooling.md`, `26-migration-strategies.md`,
`27-multi-tenancy.md`, `28-database-security.md`,
`29-time-series-optimization.md`, and `30-stream-processing.md`.
These topics are the natural follow-on because they share database workload,
recovery, and capacity assumptions with Batch 1 and benefit from consistent
terminology and cross-links.

### Batch 2A — database operations and scale (approved)

Batch 2A is the first ordered implementation slice of Batch 2. Terra's final
gate passed for all eight guides on 2026-09-01. Preserve Batch 1's approved
records above; maintainer confirmation and the remaining batches remain open.

| Sequence | Exact path | Requirements / gate |
| ---: | --- | --- |
| 1/8 | `docs/02-databases/17-query-planning.md` | 400–550 lines; optimizer and join/spill Mermaid; reproducible planner diagnosis; 2 tables; 4 exercises; 8–10 Q&As |
| 2/8 | `docs/02-databases/25-connection-pooling.md` | 300–425 lines; client→pooler→server Mermaid; capacity model and PgBouncer caveats; 1 table; 3 exercises; 6–8 Q&As |
| 3/8 | `docs/02-databases/24-database-monitoring.md` | 400–550 lines; SLO/burn-rate example; telemetry/correlation Mermaid; scoped `pg_stat_database` counters; 2 tables; 4 exercises; 8–10 Q&As |
| 4/8 | `docs/02-databases/16-backup-recovery.md` | 400–550 lines; 2 TB/5-minute/4-hour RPO/RTO model; PITR/recovery Mermaid; immutable/key/ransomware/corruption coverage; 2 tables; 4 exercises; 8–10 Q&As |
| 5/8 | `docs/02-databases/21-eventual-consistency.md` | 400–550 lines; multi-region profile/version/session-token example; stale-read/repair Mermaid; qualified CAP/session guarantees; 2 tables; 4 exercises; 8–10 Q&As |
| 6/8 | `docs/02-databases/19-sharding-advanced.md` | 450–600 lines; tenant/order skew and capacity model; routing/rebalance Mermaid; fencing, global-index, and cross-shard caveats; 2 tables; 4 exercises; 8–10 Q&As |
| 7/8 | `docs/02-databases/26-migration-strategies.md` | 450–600 lines; high-write expand-contract example and compatibility matrix; resumable validation and rollback boundary; state-machine Mermaid; 2 tables; 4 exercises; 8–10 Q&As |
| 8/8 | `docs/02-databases/28-database-security.md` | 500–650 lines; tenant PII path; defense-in-depth/envelope-encryption Mermaid; KMS/RLS/audit/TLS/provider caveats; 2 tables; 4 exercises; 8–10 Q&As |

Every Batch 2A guide must also retain the common contract: explicit metadata
(`Level`, `Status: draft`, `Audience`, `Prerequisites`, `Sequence: Batch 2A n/8`,
and `Terra gate: open`), 3–6 measurable objectives, exact headings for What it
is, Why it matters, Mental model, Worked example, Advantages and limitations,
Topic-specific visual, Failure modes and operations, Practical exercises,
Interview Q&A, and Related and next reading. Each visual needs interpretation;
each exercise needs a solution or expected approach; each Q&A needs Answer and
Follow-up; assumptions, units, and provider/version caveats must be stated.

The strict repository profile is `python3 scripts/audit_documentation.py
--profile batch-2a --fail-on-missing --summary`. Its eight per-guide Terra
sign-offs are recorded below after the final gate passed:

| Guide | Guide status | Terra gate | Reviewer | Date | Decision/corrections | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/02-databases/17-query-planning.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/25-connection-pooling.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/24-database-monitoring.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/16-backup-recovery.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/21-eventual-consistency.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/19-sharding-advanced.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/26-migration-strategies.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |
| `docs/02-databases/28-database-security.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Terra final gate passed; maintainer confirmation remains open |

### Batch 2B — analytical data paths and tenant boundaries (approved)

Batch 2B is the second ordered implementation slice of Batch 2. It follows
Batch 2A's operational foundations with physical layouts, analytical pipelines,
time-series retention, search read models, caches, event movement, and
tenant-aware isolation. Terra's final gate passed for all eight guides on
2026-09-01; all eight are recorded as `Status: reviewed` with
`Terra gate: approved`. The order is intentional:
columnar layout supports warehouse and time-series storage; optimization follows
time-series fundamentals; search and caching build derived read paths; queues
explain replay and delivery boundaries; multi-tenancy composes those boundaries
with authorization and operations.

| Sequence | Exact path | Draft implementation target |
| ---: | --- | --- |
| 1/8 | `docs/02-databases/04-columnar-databases.md` | 450–600 lines; row/column layout, segment metadata, encodings, vectorized execution, pruning/write cost, scan-bytes calculation, small-file/skew/mutation operations; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 2/8 | `docs/02-databases/10-warehousing-lakehouses.md` | 500–650 lines; warehouse/lake/lakehouse, storage versus table formats, CDC/backfill Bronze–Silver–Gold replay, late-order/schema-change correction, duplicate/partial/schema/governance/scan failures; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 3/8 | `docs/02-databases/05-timeseries-databases.md` | 450–600 lines; samples, labels, series cardinality, ingest/retention/query/alerts, derived volume, WAL/head/blocks/compaction, cardinality/clock/out-of-order/backpressure failures, binary/decimal units; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 4/8 | `docs/02-databases/29-time-series-optimization.md` | 400–525 focused lines; chunks/compression, rollups, tiering, late data, raw-versus-rollup fidelity, hot/warm/cold, raw-to-rollup late correction, SLO storage/query trade-off, downsampling/compaction/DST failures; 2 tables, 2 Mermaid diagrams, 3 exercises, 6–8 Q&A |
| 5/8 | `docs/02-databases/06-search-engines.md` | 500–650 lines; analyzers, inverted segments, ranking/filtering/facets, refresh/shards/replicas, source→CDC→index→refresh→query/rerank, product-search evaluation, mapping/reindex/shard/stale/synonym/relevance failures and three freshness dimensions; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 6/8 | `docs/02-databases/07-caching-stores.md` | 500–650 lines; source of truth, cache-aside/write-through/write-behind, negative cache, TTL jitter, eviction/persistence/failover, miss/fill/invalidation/fallback, TTL/DB-protection calculation, stampede/hot-key/stale/lost-write/split-brain/poison/tenant-leakage failures; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 7/8 | `docs/02-databases/11-message-queues-streams.md` | 500–650 lines; queue/pub-sub/durable log/event sourcing/stream processing, outbox→partition→consumer group→idempotent sink/DLQ, duplicate/retry/replay/reconciliation/order trace, delivery/order/idempotency/side-effect/retention/schema/rebalance failures; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |
| 8/8 | `docs/02-databases/27-multi-tenancy.md` | 500–650 lines; end-to-end isolation, shared schema/RLS versus schema/database per tenant, placement/quotas/routing/onboarding/offboarding/migrations, authenticated request→tenant context→pool reset→RLS/router→audit, tenant classes, RLS/BYPASSRLS/owner/pool/identifier/noisy-neighbor/backup/deletion/drift failures; 2 tables, 2 Mermaid diagrams, 4 exercises, 8–10 Q&A |

#### Batch 2B technical-risk checklist

- [x] Keep all eight metadata blocks exact: `Status: reviewed`, audience,
  prerequisites, `Sequence: Batch 2B n/8`, and `Terra gate: approved`.
- [x] Check units and arithmetic: distinguish decimal GB/TB from binary GiB/TiB;
  label logical, compressed, replicated, and temporary bytes.
- [x] Qualify observed latency, throughput, compression, cost, availability,
  and cardinality figures by workload, provider, and deployed version.
- [x] Check consistency scope: cache invalidation, index visibility, broker
  offsets, RLS, replicas, rollups, and source-of-truth boundaries must not be
  described as stronger than their actual guarantees.
- [x] Check replay and idempotency: late corrections, CDC, outbox relay,
  at-least-once delivery, DLQ replay, compaction, and tenant migration need
  durable identity and reconciliation paths.
- [x] Check failure containment: small files, skew, mutations, schema drift,
  stampedes, hot keys, poison messages, rebalances, noisy neighbors, backups,
  deletion, and partial writes have detection and recovery evidence.
- [x] Check diagrams are topic-specific and followed by interpretation; check
  comparison tables name meaningful alternatives and trade-offs.
- [x] Check every exercise has a solution/expected approach and every Q&A has
  explicit `Answer` and `Follow-up`; check at least two existing related links.
- [x] Keep Batch 1 and Batch 2A approval records unchanged. Terra approval is
  recorded in the sign-off rows below.

#### Batch 2B reviewed/approved sign-off record

| Guide | Guide status | Terra gate | Reviewer | Date | Decision/corrections | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/02-databases/04-columnar-databases.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/10-warehousing-lakehouses.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/05-timeseries-databases.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/29-time-series-optimization.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/06-search-engines.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/07-caching-stores.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/11-message-queues-streams.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |
| `docs/02-databases/27-multi-tenancy.md` | `reviewed` | `approved` | Terra | 2026-09-01 | PASS — Terra final gate passed | Maintainer confirmation remains open |

The strict structural command is:
`python3 scripts/audit_documentation.py --profile batch-2b --fail-on-missing
--summary`. It is a structural gate; Terra's PASS confirms that the
technical-risk checklist and human review passed. Terra approval is recorded
above, while maintainer confirmation remains open.

## Terra next-phase sequence

The next phases are intentionally open. Do not mark a future cohort approved,
and do not upgrade the three remaining Batch 2 guides in this reviewer-system
pass.

1. **Batch 2C — three remaining database guides:**
   `13-consensus-algorithms.md`, `22-distributed-tracing.md`, and
   `30-stream-processing.md`. Define the guide contract and obtain human review
   before enabling a strict profile.
2. **Batch 3A — ML/AI foundations:** begin with the five RAG, serving, NLP,
   cost, and rollout guides listed below; reconcile claims with the three tested
   labs and apply the ML/AI checklist.
3. **Batch 4A — paths/frameworks:** review the selected learning-path routing
   files and high-use interview frameworks, including prerequisites, outputs,
   exercises, and review checkpoints.
4. **Batch 5 — system-design debt:** review selected cohorts by directory,
   retain the structural-filler 27 and copied-capacity 134 thresholds, and
   replace copied capacity blocks with unit-checked, topic-specific material.

The registry exposes these four cohorts as `open` and non-enforced scaffolds.
Only Batch 1, Batch 2A, and Batch 2B are established green profiles.

### Batch 3A — AI/ML foundations

Review `docs/04-ai-ml-llms/` using the same template, starting with
`06-rag-systems.md`, `08-model-serving-inference.md`,
`12-nlp-advanced.md`, `16-cost-optimization.md`, and
`22-model-rollouts-and-serving.md`. Add evaluation datasets, error budgets,
data/model lineage, rollout failure modes, and links to the tested labs before
expanding into the remaining guides.

### Batch 4A — learning paths and interview frameworks

Use `learning-paths/README.md`, `learning-paths/index.md`,
`learning-paths/domains/`, `learning-paths/sequential-tracks/`, and
`learning-paths/interview-playbooks/` as the routing surface. Add explicit
prerequisites, expected outputs, exercise links, and review checkpoints. Then
apply the template to the highest-use files in
`docs/01-interview-frameworks/`, preserving the distinction between tested,
reviewed, and draft material.

### Batch 5 — system design catalog and debt cohorts

Continue by directory, beginning with the groups tracked in
`docs/03-system-design/CONTENT_STATUS.md`, then the remaining directories under
`docs/03-system-design/`. The existing 27/134 audit thresholds remain the
regression baseline while guides are rewritten. Replace copied capacity blocks
with stated assumptions, unit-checked calculations, and topic-specific
diagrams; retain the audit's debt report until each guide is reviewed.

## Acceptance criteria

For each upgraded guide:

- all nine template sections are present and substantive;
- audience, prerequisites, learning objectives, sequence, status, and Terra gate
  fields are explicit;
- the guide meets its foundational depth target unless Terra records an exception;
- at least one topic-specific Mermaid diagram has explanatory text;
- the comparison table has at least two real alternatives and names material
  consistency, latency, cost, scale, and operational trade-offs where relevant;
- the worked example states workload assumptions and avoids unqualified universal
  performance, availability, or cost claims;
- at least three practical exercises have solutions or checkable expected approaches;
- six or more interview questions include answers and follow-ups (eight is the
  Batch 1 target);
- technical accuracy review checks units, asymptotic versus observed performance,
  provider/version scope, failure semantics, and cross-guide terminology;
- links, Markdown structure, and code fences pass repository validation.

For the repository pass:

- the active inventory remains explainable from the audit (the baseline snapshot
  is 1,000; this reviewer-system pass makes the current count 1,003);
- no existing work is reset, committed, or pushed;
- system-design debt does not exceed structural-filler 27 or copied-capacity 134;
- the full test and validation commands below pass.

## Verification commands

Run from the repository root:

```bash
pytest -q
python3 scripts/validate_repo.py --imports
python3 scripts/audit_system_design.py --max-structural-filler 27 --max-copied-capacity 134
python3 scripts/audit_documentation.py --summary
python3 scripts/audit_documentation.py --profile batch-1 --fail-on-missing --summary
python3 scripts/audit_documentation.py --profile batch-2a --fail-on-missing --summary
python3 scripts/audit_documentation.py --profile batch-2b --fail-on-missing --summary
python3 scripts/audit_documentation.py --profile batch-2c --summary
python3 scripts/audit_documentation.py --profile batch-3a --summary
python3 scripts/audit_documentation.py --profile batch-4a --summary
python3 scripts/audit_documentation.py --profile batch-5 --summary
python3 scripts/audit_documentation.py --json > /tmp/documentation-audit.json
git diff --check
```

For a human-readable per-file report, use:

```bash
python3 scripts/audit_documentation.py --detailed
```

The documentation audit uses only Python's standard library. It removes fenced
code from prose-signal detection where possible, while separately recognizing
Mermaid and code/example fences. In CI, consume `--json` and fail on missing
signals with `--fail-on-missing` when a stricter gate is appropriate.
