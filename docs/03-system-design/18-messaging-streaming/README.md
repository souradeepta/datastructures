# Messaging and Streaming Labs

- [Event-time windows and watermarks](41_event-time-watermarks.md) —
  [implementation](../../../python/distributed_systems/event_time_windows.py)
  and [tests](../../../tests/distributed_systems/test_event_time_windows.py)

Use the lab to practice event-time versus processing-time semantics, tumbling
window boundaries, deduplication, watermarks, allowed lateness, and late-data
side outputs. It deliberately omits a broker, checkpointing, state recovery,
parallel partitions, and exactly-once delivery.
