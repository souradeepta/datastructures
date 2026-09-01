# API gateway

An API gateway is an edge component that applies a consistent boundary around
backend services. It may perform authentication, rate limiting, transformation,
and routing in production. This focused exercise isolates exact-path routing so
the behavior can be tested without pretending to implement all of those
concerns.

## Runnable contract

The api_gateway.py model maps non-empty exact paths to named callable Service
objects. Its behavior is covered in test_api_gateway.py.

- register(path, service) rejects invalid paths and invalid services.
- A duplicate path is rejected unless replace=True is supplied.
- route(path, request) invokes the matching service and returns its response.
- Unknown paths raise KeyError; service exceptions propagate to the caller.
- replace(path, service) is an explicit convenience operation.

The model does not implement authentication, authorization, rate limiting,
retries, load balancing, protocol translation, persistence, or concurrency
control. It is an in-memory routing exercise, not an edge proxy.

## Gateway versus BFF

A shared gateway centralizes cross-cutting policy and gives clients one public
boundary. A backend-for-frontend (BFF) instead gives a client type—web,
mobile, or partner—an API shaped for its needs. A large gateway can become a
deployment and ownership bottleneck; several BFFs can duplicate policy.
Choose ownership and failure isolation deliberately.

## Request flow

~~~text
client -> gateway -> exact route lookup -> service(request) -> response
                  \-> metrics and tracing in production
~~~

Keep route matching rules explicit. Exact matching is easy to test. Prefix,
version, method, host, and content-negotiation matching are useful extensions,
but each adds precedence rules and opportunities for ambiguous routes. Never
silently trim or normalize a path unless that is part of the contract.

## Production responsibilities

A production gateway commonly adds:

- authentication and authorization before forwarding;
- per-client and per-route rate limits;
- deadlines, bounded retries, and circuit breakers;
- load balancing and health-aware endpoint selection;
- request size limits, schema validation, and protocol translation;
- access logs, traces, redaction, and latency/error metrics.

Each feature affects availability and latency. For example, retrying a failed
backend can improve success probability for transient errors while increasing
load and tail latency. Authentication at the gateway simplifies enforcement,
but services still need authorization for defense in depth.

## Worked traffic estimate

Assume 12,000 requests/second, an average 3 KB request, and an 8 KB response.

- Request payload ingress = 12,000 × 3 KB = 36,000 KB/s, or 36 MB/s.
- Response payload egress = 12,000 × 8 KB = 96,000 KB/s, or 96 MB/s.
- Combined application payload crossing the gateway is about 132 MB/s, before
  TLS, headers, buffering, and observability traffic.
- If one instance safely handles 4,000 requests/second, three instances meet
  the average rate (12,000 / 4,000). To hold 30% headroom, capacity should be
  15,600 requests/second, requiring four instances at that per-instance rate.

These are planning inputs, not a performance promise. Benchmark the chosen
proxy and service handlers with realistic payloads, connection reuse, TLS, and
failure rates.

## Interview prompts

- Which policies belong at the edge and which must remain in the service?
- How do route changes roll out without sending traffic to incompatible code?
- What happens when the gateway is healthy but one backend is degraded?
- How do you preserve trace context and redact sensitive request data?
