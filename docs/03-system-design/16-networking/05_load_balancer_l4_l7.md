# Load Balancer: Layer 4 vs Layer 7

## Objective

Distribute connections or requests across healthy backends while limiting
overload and providing predictable failover. The layer at which the balancer
operates determines what it can observe and change.

| Layer | Sees | Typical capabilities |
|---|---|---|
| L4 | IP, protocol, ports, connection state | Fast connection distribution, NAT or tunneling |
| L7 | HTTP/TLS termination, host, path, headers | Routing rules, retries, authentication hooks, request metrics |

L7 is more programmable but must parse and often terminate connections. L4 is
usually cheaper per packet and preserves more end-to-end behavior.

## Request and connection flow

```text
client → listener → health-aware strategy → backend
   │                                  └─ connection/request counters
   └─ timeout, retry, and overload policy
```

Round robin is predictable for similar backends. Weighted round robin accounts
for capacity. Least connections can help when request durations vary, but the
counter must represent active work accurately. Randomized or power-of-two
choices can reduce coordination at large scale.

Health checks should test the dependency level required for traffic, use
timeouts and consecutive-failure thresholds, and remove unhealthy backends
without making an already overloaded pool flap. Retries need a budget and
should normally be limited to idempotent operations.

## L4, L7, and DSR choices

| Design | Advantages | Costs and risks |
|---|---|---|
| L4 proxy/NAT | Simple protocol handling and broad applicability | Connection state and return traffic consume balancer resources |
| L7 reverse proxy | Content routing, TLS termination, rich observability | Parsing/TLS CPU, larger software attack surface, retry semantics |
| Direct Server Return (DSR) | Backend sends responses directly to the client, reducing return-path work at the balancer | Requires routing, address ownership, and network symmetry to be designed carefully |

DSR does not universally reduce bandwidth by a fixed factor. The result depends
on whether the balancer forwards packets, performs NAT, terminates TLS, and how
the network routes the backend response. State those assumptions before sizing.

## Load-balancer-specific sizing example

Assume a peak of 20,000 new connections/second and 200,000 concurrent
connections. For this simplified model, also assume 20,000 requests/second
(one request per new connection during the measured interval), a 2 KB average
request payload, and a 20 KB average response payload. For an L7 full proxy,
the application payload crossing the client-facing path is:

```text
request traffic  = 20,000 × 2 KB  = 40 MB/s
response traffic = 20,000 × 20 KB = 400 MB/s
```

Because a full proxy receives and sends both directions, its aggregate NIC
traffic is approximately `2 × (40 + 400) = 880 MB/s`, or about 7.0 Gbit/s,
before TLS, headers, retransmits, and health checks. A DSR design may remove
most response bytes from the balancer’s return path, but the backend network
and the client route still carry them.

The connection table also matters: at an illustrative 256 bytes of balancer
state per connection, 200,000 concurrent connections consume about 51 MB
before allocator and kernel overhead. TLS termination is CPU- and
implementation-dependent; benchmark handshakes, resumed sessions, cipher
suites, and target p99 latency instead of converting request rate directly to
a fixed core count.

For 100 backends checked every five seconds, one check per backend is about
20 checks/second. At 2 KB per check, that is only about 40 KB/s of probe
payload, but probes still need isolated timeouts and must not overload a
fragile health endpoint.

## Implementation and practice

The repository example demonstrates round-robin, least-connections, random
selection, health filtering, and removal in
[python/system_design/load_balancer.py](../../../python/system_design/load_balancer.py).
Focused tests are in
[tests/system_design/test_load_balancer.py](../../../tests/system_design/test_load_balancer.py).
It is an educational in-process selector: it does not open sockets, terminate
TLS, track real connection lifetimes, or implement production health probes.

Practice adding weighted backends, connection draining, retry budgets, circuit
breaking, and metrics for selection skew, queue depth, active connections,
backend errors, and p50/p99 latency.

## Failure handling

- Remove failed backends from new traffic while allowing existing connections
  to drain when possible.
- Bound queueing and request timeouts so one slow backend cannot exhaust all
  balancer workers.
- Use multiple balancer instances and failure domains; a single VIP or control
  plane should not be the only failure point.
- Preserve client identity only when the chosen proxy mode and privacy model
  support it; do not rely on a spoofable header without a trusted boundary.

## Interview prompts

1. When does L7 routing justify its CPU and operational cost?
2. How do you drain a backend during deployment without dropping requests?
3. What changes when connections are long-lived WebSockets or streaming RPCs?
4. How would you size and test a balancer for a response-heavy workload?
