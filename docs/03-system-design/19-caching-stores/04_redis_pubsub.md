# Redis Pub/Sub and keyspace notifications

Redis Pub/Sub is a fast broadcast channel, not a durable event log. A publisher
sends a message to a channel and Redis forwards it to subscribers currently
connected to that channel. A disconnected subscriber does not receive a
replay unless the application stores the event elsewhere.

## Runnable contract

The repository's pub_sub_system.py is a small local analogue, tested by
test_pub_sub_system.py. It makes four behaviors concrete:

- subscribing twice for the same (topic, subscriber_id) replaces the callback
  without duplicating delivery;
- publishing invokes subscribers in registration order;
- unsubscribing is idempotent and unknown reads do not create topic state;
- a callback failure is collected while later subscribers still receive the message.

The model has no persistence, replay, backpressure, concurrency control,
delivery guarantee, authentication, or Redis protocol behavior. It has no
print side effects so callers can choose their own logging and metrics.

## Pub/Sub versus Streams

| Mechanism | Replay | Consumer coordination | Appropriate use |
| --- | --- | --- | --- |
| Redis Pub/Sub | No | Subscribers each receive broadcasts | ephemeral presence or UI hints |
| Redis Streams | Yes, while retained | Consumer groups and pending entries | work processing and recovery |
| Durable broker | Usually yes | partitions, offsets, retention policies | high-volume event history |

Cache invalidation is a common Pub/Sub use case, but a missed invalidation can
leave stale data indefinitely. Safer designs pair the notification with a
versioned database record, a TTL, or a stream/outbox that can be replayed.

## Keyspace notifications

Keyspace notifications are server-side events emitted for selected key
operations. They are useful for development tools and best-effort cache
observers, but they consume CPU and network bandwidth and are not a substitute
for an audit log. Choose the event classes narrowly, treat notifications as
lossy, and avoid putting sensitive values into channels.

## Failure and operations

A slow subscriber can accumulate outbound buffers and increase memory pressure.
Monitor connection count, output-buffer growth, publish latency, dropped or
missed events, and reconnect rates. On reconnect, a client should resync from a
source of truth rather than assume it received every message.

A production broadcast path should define:

- maximum message size and serialization format;
- whether one subscriber's failure is isolated;
- reconnect and resynchronization behavior;
- channel naming and tenant authorization;
- whether fan-out is local, regional, or cross-region.

## Worked fan-out estimate

Assume 50,000 messages/second, an average 1.5 KB serialized message, and
100 active subscribers per channel on average.

- Publisher ingress payload = 50,000 × 1.5 KB = 75,000 KB/s, or 75 MB/s.
- Subscriber egress payload = 75 MB/s × 100 = 7,500 MB/s, or 7.5 GB/s.
- At 1,000 subscribers per channel, the same workload would be 75 GB/s of
  subscriber payload before protocol, TLS, replication, and framing overhead.

The multiplication by subscriber count is the important scaling property:
broadcast cost is driven by fan-out, not just publish rate. Shard channels or
use regional relays when one process cannot manage the connection and egress
budget.

## Interview prompts

- What events may be lost, and how does a client repair its state?
- When should Redis Streams or a durable log replace Pub/Sub?
- How do you prevent a noisy tenant from consuming the whole output buffer?
- What is the authorization boundary for channel names?
