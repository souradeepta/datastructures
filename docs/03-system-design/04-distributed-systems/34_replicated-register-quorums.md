# Replicated Register and Quorums

**Audience:** L4–L5 system-design candidates. **Practice time:** 25 minutes.

## Objective

Explain why a read quorum `R` and write quorum `W` intersect when `R + W > N`,
then use the lab to reason about unavailable replicas, stale values, and read
repair.

```text
client -> coordinator -> { replica A, replica B, replica C }
                         write W acknowledgements
                         read R responses -> newest version -> repair
```

## Model contract

[`QuorumRegister`](../../../python/distributed_systems/quorum_register.py)
stores immutable, versioned values in memory. A write contacts `W` currently
available replicas and fails before changing state if fewer are available. A
read contacts `R` available replicas, selects the highest version, and updates
older replicas in that read set. Replica availability is toggled explicitly to
simulate a partition. Mutable values are copied at the API boundary.

The constructor rejects invalid quorum sizes and configurations without
intersection. This is quorum safety, not linearizability: there is no real
network, clock, leader, durable log, conflict resolver, or concurrent operation.

## Trade-offs and failure modes

| Choice | Benefit | Cost |
|---|---|---|
| Larger `W` | More durable completed writes | Higher write latency and lower write availability |
| Larger `R` | Better chance of seeing the newest version | Higher read latency and lower read availability |
| Read repair | Converges replicas when reads encounter staleness | Adds write traffic to reads and repairs only contacted replicas |
| Quorum replication | Availability during some failures | Does not solve Byzantine behavior or durable recovery |

For `N=3`, `R=2`, and `W=2`, at most one replica can be unavailable while a
quorum operation continues. A partition that leaves only one replica cannot
complete either operation. Production systems also need hinted handoff,
anti-entropy, tombstones, request IDs, durable versions, and a clearly chosen
consistency model.

## Interview prompts

1. Why does `R + W > N` imply an overlap, and what does the overlap guarantee?
2. What changes if versions are wall-clock timestamps and clocks move backward?
3. How would you prevent a repaired stale value from overwriting a newer one?
4. When would a leader-based consensus log be preferable to quorum registers?

**Exercise:** change the model to expose repair work as a queue and explain how
anti-entropy would heal replicas that no read contacts.
