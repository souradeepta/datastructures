# LRU Cache

## Objective

Design a bounded cache that returns a value in O(1) and evicts the item that
has been unused for the longest time. A `get` counts as use; a `put` of an
existing key updates its value and makes it most recently used.

This is an in-memory component. A distributed cache needs additional decisions
about partitioning, replication, invalidation, and failure recovery.

## Requirements

- `get(key)` returns the value or a miss sentinel and updates recency.
- `put(key, value)` inserts or updates an item and evicts when full.
- The number of entries never exceeds the configured capacity.
- Both operations are O(1) average time and use O(capacity) space.

## Design

Combine two structures:

1. A hash map maps each key to its cache node.
2. A doubly linked list stores nodes from most recently used to least
   recently used.

```text
hash map: key ───────────────► node

head (MRU) ⇄ node ⇄ node ⇄ node ⇄ tail (LRU)
```

On a hit, remove the node from its current position and place it after the
head. On insertion, add a node at the head. If the cache is over capacity,
remove `tail.prev` from both the list and the map. Updating an existing key
uses the same move-to-head operation.

## Request flow

```text
get(key)
  ├─ miss → return -1
  └─ hit  → unlink node → move to MRU → return value

put(key, value)
  ├─ existing → update → move to MRU
  └─ new      → add to MRU → if full, remove LRU
```

The cache-aside pattern usually wraps this component: read the cache first,
load the backing store on a miss, then populate the cache. Request coalescing
or jittered expiration can reduce a thundering herd when a hot key expires.

## Implementation and practice

The runnable educational implementation uses a hash map and sentinel-headed
linked list: [python/system_design/lru_cache.py](../../../python/system_design/lru_cache.py).
Its focused behavior tests are in
[tests/system_design/test_lru_cache.py](../../../tests/system_design/test_lru_cache.py).

Useful edge cases to test:

- capacity one;
- repeated `put` for the same key;
- a miss on an empty cache;
- a `get` changing which entry is evicted;
- invalid or zero capacity, if the API chooses to reject it.

## Complexity

| Operation | Average time | Extra space |
|---|---:|---:|
| `get` | O(1) | O(1) |
| `put` | O(1) | O(1) per new entry |
| Entire cache | — | O(capacity) |

## Cache-specific sizing example

Treat these numbers as an illustrative model, not a capacity guarantee. Assume
1,000,000 resident entries, a 32-byte key, a 1,024-byte payload, and 64 bytes
for pointers, timestamps, allocator slack, and other metadata:

```text
logical entry size = 32 + 1,024 + 64 = 1,120 bytes
logical resident data ≈ 1,000,000 × 1,120 ≈ 1.12 GB (decimal)
planning size with 30% overhead ≈ 1.46 GB
```

If the node has a 1.5 GB cache budget, a capacity of one million entries is
near the limit; leave more headroom if payload sizes vary or the runtime has
significant object overhead. Measure actual resident size rather than relying
on the simplified metadata estimate.

For 200,000 requests/second and a 90% hit rate:

```text
cache hits  ≈ 180,000 requests/second
backing-store misses ≈ 20,000 requests/second
```

The hit rate is workload-dependent. If the working set is larger than the
budget, recency churn can make an LRU cache ineffective. Track hit rate,
evictions, item size, memory utilization, miss latency, and backend load. A
lower hit rate may call for a larger cache, a different policy such as LFU, or
better key normalization—not automatically more replicas.

## Scaling and trade-offs

| Choice | Strength | Cost or risk |
|---|---|---|
| In-process LRU | Lowest latency and simple failure model | Each service instance has a separate, bounded copy |
| Shared Redis/Memcached cache | Shared working set and independent scaling | Network latency, node failure, partitioning, and hot keys |
| Sharded cache | Higher aggregate memory and throughput | Key movement, rebalancing, and uneven hot-key load |
| LRU | Good for temporal locality | Can evict frequently used but temporarily idle items |
| LFU or adaptive policy | Better for stable frequency-heavy workloads | More bookkeeping and slower adaptation to workload changes |

For concurrent access, protect the map and list mutation as one operation, or
shard the cache and accept per-shard ordering. Decide whether stale values are
acceptable, how writes invalidate entries, and whether a cache outage should
fail open to the backing store or shed load.

## Interview prompts

1. How would you prevent a hot-key stampede after expiration?
2. What changes when the cache is sharded across regions?
3. When would LFU, TTL, or a write-through cache be preferable to LRU?
4. Which metrics would tell you that the cache is too small or too large?
