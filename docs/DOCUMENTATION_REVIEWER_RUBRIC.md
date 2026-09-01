# Documentation Reviewer Rubric

**Status:** canonical reviewer guidance
**Owner:** repository maintainers
**Reviewer:** Terra for curriculum gates; a maintainer for final confirmation
**Scope:** active Markdown guides, learning paths, and interview frameworks

This is the human-review standard for the documentation upgrade. It is the
companion to the machine-readable profile registry in
[`scripts/documentation_profile_definitions.py`](../scripts/documentation_profile_definitions.py)
and the structural scanner in
[`scripts/audit_documentation.py`](../scripts/audit_documentation.py). The
rubric records what a reviewer must decide; a green scanner is evidence for
structure, not a substitute for that decision.

## Gate states

Use the states below exactly and keep the guide status separate from the Terra
gate. A gate is not closed merely because a file exists or a command passes.

| Guide status | Terra gate | Meaning | Allowed claim |
| --- | --- | --- | --- |
| `draft` | `open` | Work is useful or under review, but the reviewed standard has not passed. | Treat as draft/illustrative. |
| `reviewed` | `approved` | Terra completed the relevant content gate and recorded a pass. | Terra-approved guide; maintainer confirmation may still be pending. |
| `reviewed` | `pending` | Human review is substantially complete but a named approval or correction is outstanding. | Do not call the guide approved. |
| `tested` | `n/a` | A focused implementation test exercises an educational example. | Tested example only; not a reviewed guide or production claim. |
| any | `blocked` | A material correctness, ownership, or evidence issue prevents approval. | State the blocker and next evidence needed. |

`reviewed/approved` is the only Terra approval pair. Do not infer approval from
`tested`, a passing profile, a checklist with unchecked items, or an inventory
count. Maintainer confirmation remains pending for the existing Terra-approved
Batch 1, Batch 2A, and Batch 2B records until a maintainer explicitly closes it.

## Human decision rubric

Review each dimension as **PASS**, **CORRECTION**, or **BLOCKED**. A cohort may
be recorded as Terra-approved only when every required dimension is PASS or an
explicit, documented exception names its owner and follow-up. A correction is a
content change to make before approval; a blocker is a claim or omission that
cannot be accepted as-is.

| Dimension | PASS requires | Typical correction/blocker |
| --- | --- | --- |
| Curriculum | Objective, audience, prerequisites, sequence, depth, and next reading fit the learning path. | A guide promises production expertise while teaching only a toy; prerequisites or outputs are missing. |
| Technical accuracy | Definitions, algorithms, APIs, units, calculations, and code match the stated scope and version. | Universal latency/availability/cost claim; unexplained arithmetic; provider behavior presented as a standard. |
| Distributed systems | Consistency, ordering, failure, retry, idempotency, recovery, and operational boundaries are explicit. | “Exactly once” or failover claim has no scope; replay duplicates side effects; partition behavior is omitted. |
| ML/AI | Dataset and model lineage, evaluation, leakage, drift, safety, rollout, cost, and serving boundaries are explicit where relevant. | Offline metric treated as production quality; training/serving skew or rollback is absent. |
| Diagrams | Every diagram is topic-specific, readable, syntactically plausible, and interpreted in prose. | Copied client/server picture, unlabeled guarantee boundary, or diagram without an invariant. |
| Exercises | Exercises have a stated task, assumptions, expected output, and checkable solution/approach. | Prompt is only “discuss”; no edge cases, calculation, or recovery criterion. |
| Q&A | Questions test theory, practice, scale, and trade-offs; each has an answer and a probing follow-up. | Trivia-only questions, answer hidden in the question, or follow-up that does not probe reasoning. |
| Claims | Material numbers and product claims have scope, assumptions, date/version, and source or qualification. | Benchmark detached from workload; capacity copied across unrelated topics. |
| Links | Local links resolve, anchors are useful, and related reading supports the intended sequence. | Dead link, self-link, archive link presented as current, or a navigation loop. |

## Review checklists

### Curriculum checklist

- [ ] Audience and prerequisite knowledge are explicit.
- [ ] Three to six measurable learning objectives describe reader outcomes.
- [ ] The sequence places the guide correctly and links to at least two useful next readings.
- [ ] The guide distinguishes conceptual explanation, worked example, practice, and interview transfer.
- [ ] Depth and line targets are appropriate to the cohort; length is not treated as quality by itself.
- [ ] Status and gate metadata are truthful and singular.
- [ ] The guide says when a toy or in-memory example is not production infrastructure.

### Technical checklist

- [ ] Definitions and terminology agree with neighboring guides.
- [ ] Complexity statements distinguish asymptotic bounds from observed performance.
- [ ] Arithmetic shows units and labels decimal versus binary bytes, logical versus physical data, replicas, WAL, and temporary space where relevant.
- [ ] Assumptions identify workload, scale, provider, version, region, and measurement method when those affect the claim.
- [ ] Examples include edge cases, validation, and a rollback or correction boundary where applicable.
- [ ] Code snippets are internally consistent with the maintained Python contract and do not imply untested guarantees.

### Distributed-systems checklist

- [ ] The source of truth and consistency model are named.
- [ ] Ordering, delivery, deduplication, idempotency, and side effects are separated.
- [ ] Timeouts, retries, backoff, leases, fencing, and replay behavior have bounded failure semantics.
- [ ] Partitions, stale reads, split brain, partial writes, overload, and dependency failure are considered.
- [ ] Recovery includes durable identity, reconciliation, observability, and an operator decision boundary.
- [ ] Capacity and availability claims state quorum, replica, region, and dependency assumptions.

### ML/AI checklist

- [ ] Data, feature, prompt, model, embedding, and evaluation-set lineage is clear.
- [ ] Train/validation/test separation and leakage boundaries are addressed.
- [ ] Metrics include a measurement population, baseline, threshold, and known failure modes.
- [ ] Drift, freshness, bias/safety, privacy, and human/operational escalation are addressed when relevant.
- [ ] Serving covers latency/cost budgets, versioning, canarying, rollback, and training-serving skew.
- [ ] Retrieval or generation claims distinguish a teaching simulation from a real model, index, or deployment.

### Diagram checklist

- [ ] The Mermaid block is topic-specific and has stable, descriptive IDs.
- [ ] Arrows, states, and boundaries show the mechanism—not merely named components.
- [ ] Important edges label events, guarantees, data identity, or failure behavior.
- [ ] Prose immediately after the diagram states the invariant, trade-off, or failure surface.
- [ ] A second diagram is used when the cohort contract requires both architecture and sequence/state/recovery views.

### Exercise checklist

- [ ] The prompt gives a bounded scenario and enough assumptions to solve it.
- [ ] Expected output includes a decision, calculation, design, code behavior, or diagnostic evidence.
- [ ] The solution or expected approach checks correctness, edge cases, complexity, and trade-offs.
- [ ] At least one exercise covers failure, recovery, migration, or operational judgment when relevant.
- [ ] Exercise links point to maintained implementations or tests when such examples exist.

### Q&A checklist

- [ ] Questions cover fundamentals, implementation, scale, failure modes, and alternatives.
- [ ] Each answer is explicit, scoped, and not just a restatement of the question.
- [ ] Each follow-up probes assumptions, evidence, complexity, consistency, or recovery.
- [ ] Provider-specific questions name the provider/version or ask the candidate to qualify the answer.
- [ ] The Q&A count matches the cohort target without padding repetitive questions.

### Claims checklist

- [ ] Every material number has visible assumptions and consistent units.
- [ ] Benchmarks and product behavior are qualified by workload and version, or linked to authoritative documentation.
- [ ] Availability, durability, consistency, and “exactly once” language names its scope and exceptions.
- [ ] Cost claims identify what is included/excluded and avoid stale prices.
- [ ] Copied capacity blocks and generic guarantees are removed or rewritten for the topic.
- [ ] Educational simplifications are labeled as simplifications, not operational recommendations.

### Link checklist

- [ ] `python3 scripts/validate_repo.py --imports` passes active Markdown links.
- [ ] Relative targets resolve from the linking file, including anchors where used.
- [ ] At least two related links are current, relevant, and not circular filler for guide cohorts that require them.
- [ ] External sources are authoritative and stable enough for the claim; otherwise state the version/date or remove the claim.
- [ ] Historical/archive material is labeled as historical and is not used as current status evidence.

## Automation boundaries

The standard-library audit may enforce paths, headings, metadata shapes, line
ranges, counts, visible Mermaid explanations, explicit exercise/Q&A labels, and
existing local links for a named profile. The registry also records whether a
profile is established or open. These are useful regression signals, not
semantic review.

Automation must not decide that a guide is technically correct, pedagogically
useful, production-ready, safe, current for a provider, or Terra-approved. It
cannot validate Mermaid rendering in every consumer, prove a benchmark,
evaluate an ML model, assess a threat model, or replace maintainer ownership.
Passing `--summary` is an inventory result. Repository-wide missing-signal
diagnostics remain visible and non-blocking. CI may run `--fail-on-missing` only
for the established green profiles listed in the workflow; open Batch 2C,
Batch 3A, Batch 4A, and Batch 5 scaffolds must remain non-enforced until their
human contracts and review records are approved.

## Review record

For every gate, record the exact paths, reviewer, date, decision, corrections,
follow-up, and maintainer-confirmation state in the
[append-only review log](DOCUMENTATION_REVIEW_LOG.md). Preserve prior entries;
append a new dated entry when a guide is corrected or its gate changes.
