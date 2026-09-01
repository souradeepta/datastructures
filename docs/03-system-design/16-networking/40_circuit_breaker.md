# Circuit breaker pattern

A circuit breaker protects a caller from repeatedly waiting on a failing
dependency. It is a local admission decision: after enough failures, calls
fail fast for a cooling period so worker pools, connection pools, and queues
retain capacity for healthy work.

## Runnable contract

The circuit_breaker.py model is synchronous and uses consecutive failures. Its
focused behavior is covered in test_circuit_breaker.py.

- CLOSED: calls run; successful calls reset the consecutive-failure count.
- OPEN: calls are rejected with CircuitOpenError.
- HALF_OPEN: after the injected monotonic clock passes reset_timeout, one
  probe is allowed.
- A successful probe closes the circuit; a failed probe opens it again.
- Service exceptions are re-raised, so callers can distinguish dependency
  errors from a breaker rejection.

The example validates a positive failure threshold, non-negative reset
timeout, and callable clock. It intentionally does not implement concurrency
coordination, sliding windows, distributed state, or operation timeout
enforcement. Those are separate production concerns.

## State flow

~~~text
             failure threshold reached
        +------------------------------+
        |                              v
     CLOSED --success--> CLOSED      OPEN
        ^                              |
        |         successful probe     | reset timeout elapsed
        +-------------------------- HALF_OPEN
                                      |
                                      | failed probe
                                      +--------> OPEN
~~~

A breaker should be scoped to a dependency and often to an operation class.
One slow payment provider should not necessarily block an unrelated profile
lookup. A shared breaker across unrelated dependencies creates false opens;
one breaker per request can fail to protect anything.

## Tuning and interactions

The threshold is consecutive failures, not an error percentage. At 2,000 calls
per second, a 1% error rate is 20 errors per second, but those errors may be
interleaved with successes and never reach a threshold of five. Conversely, a
short burst of five failures opens immediately. Use a rolling error window when
the policy is percentage-based, but document that it is a different algorithm.

A breaker does not create a timeout. Set a dependency timeout inside the
operation, then consider the interaction with retries and bulkheads:

- retries multiply load against an already unhealthy dependency;
- a bulkhead limits the number of waiting calls;
- a timeout bounds resource occupancy;
- the breaker stops new work after its failure policy trips.

Record state transitions, rejected calls, operation latency, failure reasons,
probe outcomes, and the dependency identity. Alerting should distinguish an
open circuit from an actual recovery failure.

## Worked recovery-budget example

Suppose a dependency receives 200 calls/second and the breaker opens after five
consecutive failures with a 30-second reset timeout.

- At the configured threshold, at least five calls have failed consecutively;
  the breaker then rejects new calls locally.
- During 30 seconds of open state, up to 6,000 calls (200 × 30) can be
  rejected without reaching the dependency.
- This is an upper-bound admission count, not a guarantee: callers may stop
  sending traffic, and a half-open probe occurs when the clock allows it.

The breaker trades dependency load for caller-visible failures. Choose the
timeout from observed recovery behavior and the business's acceptable outage,
not from a generic availability target.

## Interview prompts

- Which failures count: timeouts, 5xx responses, validation errors, or all exceptions?
- Should one tenant or endpoint have an independent breaker?
- How do retries and a circuit breaker interact without creating a retry storm?
- What metrics tell you that the breaker is falsely open?
