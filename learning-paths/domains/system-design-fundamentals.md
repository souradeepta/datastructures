---
domain: system-design-fundamentals
difficulty: "⭐⭐⭐-⭐⭐⭐⭐"
estimated_time: "5-7 hours"
prerequisites: [basic data structures, HTTP, SQL fundamentals]
covered_in_stages: [technical-round]
problem_count: 8
key_concepts: [capacity planning, caching, replication, partitioning, messaging, reliability]
---

# System Design Fundamentals

**Level:** L3-L5 · **Time:** 5–7 hours

## Learning objective

Build a design answer from requirements and workload assumptions, then defend
consistency, failure, scaling, and operational trade-offs. Use the runnable
labs to make the invariants concrete.

## Progression

1. **Workload and API:** estimate traffic, storage, latency, and hot keys before
   choosing components. Practice with the [system-design interview playbook](../interview-playbooks/system-design-round.md).
2. **State and scale:** compare cache-aside and write-through caching, then
   compare range partitioning with [consistent hashing](../../docs/03-system-design/04-distributed-systems/35_partitioning-and-rebalancing.md).
3. **Consistency:** reason about replicas, `R + W > N`, stale reads, and repair
   with the [quorum register lab](../../docs/03-system-design/04-distributed-systems/34_replicated-register-quorums.md).
4. **Asynchronous work:** compare queues, pub/sub, and logs; use the
   [event-time lab](../../docs/03-system-design/18-messaging-streaming/41_event-time-watermarks.md)
   to discuss watermarks and late data.
5. **Reliability:** add timeouts, retries, idempotency, circuit breakers,
   backpressure, load shedding, and recovery plans.
6. **Close the loop:** identify metrics, alerts, security boundaries, cost
   drivers, and what changes at 10× scale.

## Interview checklist

- Clarify users, read/write ratio, freshness, durability, and regional scope.
- Draw request flow and data ownership; name the source of truth.
- State one consistency guarantee and one tolerated failure.
- Calculate with explicit units and explain a bottleneck.
- Discuss migration, rollback, observability, abuse prevention, and cost.

## Practice prompts

- Design a profile store that remains readable during one replica failure.
- Move a hot keyspace to a new shard without losing writes.
- Design an event counter when events arrive late and out of order.
- Explain why ordinary Paxos addresses crash faults, while Byzantine consensus
  needs a different protocol and fault model.

Related paths: [distributed systems](distributed-systems.md) and [AI/ML
systems](ai-ml-systems.md).
