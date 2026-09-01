# Distributed Systems Labs

This directory combines theory guides with two runnable, dependency-free
labs. A related event-time lab is maintained in
`18-messaging-streaming/README.md`. These labs model a single coordinator and
in-memory replicas so you can practice invariants and failure cases without
mistaking a toy for a service.

## Runnable labs

- [Replicated register and quorums](34_replicated-register-quorums.md) —
  [implementation](../../../python/distributed_systems/quorum_register.py)
  and [tests](../../../tests/distributed_systems/test_quorum_register.py)
- [Partitioning and consistent-hash rebalancing](35_partitioning-and-rebalancing.md) —
  [implementation](../../../python/distributed_systems/consistent_hash_ring.py)
  and [tests](../../../tests/distributed_systems/test_consistent_hash_ring.py)

## Concepts to connect

Study quorum intersection, read repair, CAP trade-offs, consistent hashing,
virtual nodes, bounded key movement, failure detection, consensus, and
partition recovery. A normal Paxos deployment tolerates crash/omission faults;
Byzantine consensus requires a Byzantine-fault-tolerant protocol and different
assumptions. Do not use “Paxos is Byzantine-safe” as a shorthand.

All code is an educational model: it has no network, durable log, clocks,
authentication, concurrent execution, membership protocol, or crash recovery.
