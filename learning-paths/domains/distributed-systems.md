---
domain: distributed-systems
difficulty: "⭐⭐⭐⭐"
estimated_time: "3-4 hours"
prerequisites: [system design fundamentals]
covered_in_stages: [technical-round]
problem_count: 3 labs
key_concepts: [quorums, replication, consistent hashing, event time]
---

# Distributed Systems Practice Path

Read the theory guides, then run the three labs in this order:

1. [Replicated register and quorums](../../docs/03-system-design/04-distributed-systems/34_replicated-register-quorums.md)
2. [Partitioning and rebalancing](../../docs/03-system-design/04-distributed-systems/35_partitioning-and-rebalancing.md)
3. [Event-time windows](../../docs/03-system-design/18-messaging-streaming/41_event-time-watermarks.md)

For each lab, explain the invariant, failure behavior, recovery mechanism, and
what a real networked implementation must add. Keep crash faults, Byzantine
faults, partitions, and application-level conflicts distinct.
