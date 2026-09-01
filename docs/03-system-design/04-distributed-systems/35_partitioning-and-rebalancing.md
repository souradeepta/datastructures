# Partitioning and Consistent-Hash Rebalancing

**Audience:** L4–L5 system-design candidates. **Practice time:** 25 minutes.

## Objective

Route keys deterministically while adding virtual nodes, then quantify how many
keys move when membership changes.

```text
hash(key) ---> clockwise point on a ring ---> primary node
                                      \\--> next distinct nodes (replicas)
```

[`ConsistentHashRing`](../../../python/distributed_systems/consistent_hash_ring.py)
uses SHA-256, sorted virtual points, clockwise wraparound, and unique replica
selection. `migration_plan(keys, old_assignments)` returns each key’s previous
and current owner so a rebalance can be measured before copying data.

## Trade-offs

Virtual nodes smooth uneven ownership and make incremental membership changes
move roughly a fraction of keys rather than all keys. More virtual nodes use
more memory and rebuild work. Consistent hashing simplifies movement but does
not itself provide replication, transactions, hot-key protection, or a safe
data-copy protocol. Range partitioning is easier to scan; hashing usually
spreads point reads better.

## Failure and rollout checklist

1. Persist the ring version and membership change.
2. Build the new ring and calculate the migration plan.
3. Copy keys, verify checksums, and dual-read during cutover.
4. Switch ownership, then garbage-collect old copies after a safety window.
5. Monitor hot partitions, copy lag, errors, and rollback readiness.

The lab is deterministic and local. It does not model network membership,
replica consistency, durable storage, concurrent migration, or capacity limits.

**Exercise:** compare movement for 10, 50, and 200 virtual nodes over 10,000
keys and explain why the result is not a guarantee for an adversarial key set.
