# Rate Limiter

## Objective

A rate limiter decides whether a request may proceed under a policy such as
“100 requests per API key per second.” It should be explicit about the key
being limited, the burst allowed, the response to denial, and the consistency
needed when requests reach multiple service instances.

## Algorithms

### Token bucket

A bucket has a maximum capacity `C`, a current token count, and a refill rate
`r` tokens/second. A request costing `k` is accepted when at least `k` tokens
are available; accepting it removes those tokens. Between requests:

```text
tokens = min(C, tokens + elapsed_seconds × r)
```

The bucket permits a burst up to `C` while bounding the long-term rate to `r`.
It is a good default for APIs and can charge different costs for expensive
operations.

### Sliding window

A sliding-window log stores recent timestamps and removes entries older than
the window. It is precise but can use O(requests in the window) memory. A
sliding-window counter uses fixed sub-windows for bounded memory, at the cost
of some boundary approximation.

| Algorithm | Strength | Trade-off |
|---|---|---|
| Token bucket | O(1), supports controlled bursts | Requires rate and capacity tuning |
| Sliding log | Precise window | More memory and cleanup work |
| Sliding counter | Bounded memory | Boundary estimates are approximate |

## Distributed design

```text
client → gateway/service → atomic limiter state → allow or 429
                                  │
                                  └─ Redis cluster, sharded by limit key
```

The limiter key can combine dimensions, for example
`tenant:{tenant_id}:user:{user_id}:route:{route}`. Keep the policy separate
from the counter so limits can change without changing the algorithm.

For a shared Redis token bucket, the read-refill-check-write sequence must be
one atomic operation. A Lua script or a server-side function should:

1. read tokens and the last-refill timestamp;
2. compute elapsed refill using one consistent time source;
3. deduct the request cost only when enough tokens exist;
4. write both values and return allow/deny plus retry information.

Do not implement this as separate `GET`, arithmetic, and `SET` calls: two
gateways can otherwise spend the same token. A fixed-window counter can use an
atomic increment and an expiration, but its first request must establish the
TTL atomically as well.

## TTL and cleanup

Expire idle per-key state so a key that stops making requests does not consume
memory forever. A practical TTL is at least the time needed for a bucket to
refill or the policy window, with a small operational margin. Refresh it when
the key is evaluated. Monitor evictions and near-capacity memory: Redis key
expiry is cleanup, not a substitute for capacity planning.

## Implementation and practice

The local token-bucket and sliding-window examples are in
[python/system_design/rate_limiter.py](../../../python/system_design/rate_limiter.py),
with focused tests in
[tests/system_design/test_rate_limiter.py](../../../tests/system_design/test_rate_limiter.py).
They model one process and wall-clock time; a production limiter needs atomic
shared state, clock discipline, observability, and a defined failure policy.

Test burst capacity, refill after time passes, denial and retry behavior,
window expiry, multiple independent keys, and a no-backend/degraded mode.

## Illustrative request-rate model

This model is deliberately illustrative. Assume 2,000,000 active limit keys,
each averaging 20 requests/second, with a 3x peak multiplier:

```text
average checks = 2,000,000 × 20 = 40,000,000 checks/second
peak checks    = 40,000,000 × 3 = 120,000,000 checks/second
```

If every request performs one atomic check, the datastore must sustain the
peak check rate after accounting for replication, retries, and uneven hot-key
traffic. Shard by key, keep a local limiter for coarse protection, or enforce
limits at the edge to reduce central load. Benchmark the chosen datastore;
there is no universal “Redis handles N checks/second” number.

State sizing is similarly workload-specific. If 10,000,000 active keys need an
estimated 256 bytes each after datastore overhead, logical state is about
2.56 GB. Two copies require about 5.12 GB before failover and headroom; plan
capacity from measured encoded values and actual key overhead.

## Multi-region trade-offs

| Model | Benefit | Cost |
|---|---|---|
| Home-region ownership | Exact ordering for a key | Cross-region latency and failover routing |
| Local independent buckets | Low latency and regional resilience | A client can exceed a global limit across regions |
| Quota allocation per region | Bounded global budget without every-request coordination | Rebalancing unused quota and handling region failure |
| Eventually synchronized counters | Availability during link failures | Temporary overshoot and harder enforcement |

Choose fail-open or fail-closed behavior intentionally. Failing open protects
availability but weakens abuse controls; failing closed protects the backend but
can reject legitimate traffic during a limiter outage. Return `429 Too Many
Requests` with a useful retry signal, and monitor allowed, denied, latency,
state-store errors, clock skew, and hot keys.

## Interview prompts

1. How would you enforce per-IP, per-user, tenant, and endpoint limits together?
2. What happens when a Redis shard fails during a burst?
3. How would you prove that a global quota is not overspent across regions?
4. Which limits should be strict, and which can tolerate temporary overshoot?
