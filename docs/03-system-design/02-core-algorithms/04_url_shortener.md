# URL Shortener

## Objective

Map a long URL to a short, durable identifier and redirect a client from the
identifier to the original URL. The design must define uniqueness, retention,
abuse controls, redirect behavior, and whether shortening the same URL twice
returns the same code.

## Core design

```text
create:   client → API → ID allocator → URL record store
redirect: client → edge/cache → URL record store → 301/302 Location
```

An allocator can issue a monotonically increasing ID, a database sequence, or
a distributed ID. Encode the ID with Base62 for a compact path-safe code. A
distributed deployment must ensure IDs are unique across writers; a process
local counter is only an educational example.

The redirect path is read-heavy, so cache hot mappings and use a read-optimized
store. A `301` may be cached aggressively by clients and intermediaries; use
`302` when destination changes, analytics attribution, or revocation requires
more control. Validate schemes, limit destination length, scan or report abuse,
and protect the create endpoint from automated spam.

## Implementation and practice

The repository’s implementation is intentionally educational: it uses an
in-process counter and dictionaries for the mapping and reverse lookup. See
[python/system_design/url_shortener.py](../../../python/system_design/url_shortener.py)
and its focused tests in
[tests/system_design/test_url_shortener.py](../../../tests/system_design/test_url_shortener.py).
It is not a durable or concurrent service without replacing those components.

Practice collision handling, duplicate URL policy, unknown codes, malformed
URLs, expiration, and concurrent creation. Discuss how analytics events are
recorded without slowing the redirect response.

## Consistent capacity model

Use separate rates for creates and redirects. For an illustrative workload:

```text
creates:    10,000,000/day  ≈ 116 creates/second average
redirects:   1,000,000,000/day ≈ 11,574 redirects/second average
peak factor: 10x → 1,160 creates/second and 115,740 redirects/second
```

Assume a three-year retention period, a 200-byte URL record, and 100 bytes of
index and storage metadata. The logical mapping size is:

```text
records = 10,000,000 × 365 × 3 = 10.95 billion
logical data ≈ 10.95B × 300 bytes = 3.285 TB (decimal)
3 replicas ≈ 9.855 TB, before backups and compaction overhead
with 30% operational headroom ≈ 12.8 TB planned capacity
```

The estimate excludes the variable length of real URLs, tombstones, indexes
that differ by engine, and analytics data. Measure representative records and
include backup retention separately. Redirect traffic usually drives cache,
connection, and egress sizing; it does not create another mapping record.

## Base62 namespace

With 62 symbols, a fixed six-character code has `62^6 = 56,800,235,584`
possible values. Seven characters provide `62^7 ≈ 3.52 trillion` values. A
variable-length encoding may use short codes early, but reserve capacity for
future IDs and reject or migrate before the namespace is exhausted. Sequential
codes are predictable, so use opaque or randomized IDs when enumeration would
expose sensitive information.

## Reliability and consistency

- Make creation idempotent when clients may retry; an idempotency key avoids
  duplicate records after an ambiguous timeout.
- Replicate the mapping store and monitor replication lag. A redirect should
  not read a replica that is known to be behind a just-confirmed create when
  read-after-write behavior is required.
- Cache negative lookups briefly, but prevent an attacker from filling the
  cache with random codes.
- Define deletion and expiration semantics for cached redirects and audit
  events.

## Trade-offs

| Decision | Option A | Option B |
|---|---|---|
| ID generation | Central sequence, simple ordering | Distributed IDs, higher write availability |
| Redirect status | 301, lower repeat load | 302, more control over destination changes |
| Storage | Relational store, constraints and transactions | Key-value store, simple high-volume lookup |
| Cache | Fast redirects for hot codes | Stale entries and invalidation responsibility |

## Interview prompts

1. How do you generate unique IDs across regions without a central bottleneck?
2. What consistency is required immediately after a successful shorten call?
3. How do you revoke a malicious link already cached by clients?
4. Which part of the system changes first at 100x redirect traffic?
