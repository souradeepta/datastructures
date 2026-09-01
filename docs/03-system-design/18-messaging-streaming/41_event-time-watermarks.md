# Event-Time Windows and Watermarks

**Audience:** L4–L5 streaming-system candidates. **Practice time:** 25 minutes.

## Objective

Distinguish when an event happened from when a processor received it, and use a
watermark to decide when a tumbling window is safe to emit.

```text
events (out of order) -> dedupe -> [0,10) [10,20) -> watermark -> results
                                             \-> finalized late side output
```

[`EventTimeWindows`](../../../python/distributed_systems/event_time_windows.py)
deduplicates event IDs, assigns half-open windows `[start, end)`, accepts
out-of-order events until finalization, and emits each finalized window once.
With allowed lateness `L`, a window ending at `E` finalizes when
`watermark >= E + L`. Events for finalized windows are routed to
`late_events`; duplicate IDs are ignored.

## Production trade-offs

Watermarks improve completeness but delay results. A low lateness budget lowers
latency while increasing corrections or late drops. A production stream would
need partition-aware watermarks, checkpointed state, replay, bounded state
retention, backpressure, schema evolution, and a policy for correcting already
published aggregates. “Exactly once” requires more than deduplication in this
local model.

**Exercise:** add a correction stream for late events and compare it with
retractions or upserts in a downstream materialized view.
