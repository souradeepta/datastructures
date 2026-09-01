# Message queues

A message queue decouples a producer from a worker. The producer publishes
work and the worker consumes it when capacity is available. This guide focuses
on delivery state and acknowledgements; it is not a claim that the included
Python model is a broker.

## Requirements and boundaries

A useful baseline contract is:

- topics must be created explicitly;
- publishing assigns a monotonic message ID;
- consumers receive messages in FIFO order and in bounded batches;
- consumed messages remain in-flight until acknowledged;
- acknowledgement removes a message, while negative acknowledgement can requeue it;
- an unknown topic is an error rather than an implicitly created queue.

The runnable model is [message_queue.py](../../../python/system_design/message_queue.py),
with tests in [test_message_queue.py](../../../tests/system_design/test_message_queue.py).
It is an in-memory teaching exercise and has no persistence, consumer groups,
visibility timeouts, partitions, concurrency control, or crash recovery.

## Queue, broadcast, or log?

| Choice | Delivery model | Good fit | Main trade-off |
| --- | --- | --- | --- |
| Work queue | One worker handles each message | image processing, emails | replay and ordering require explicit policy |
| Pub/sub | Each subscriber receives a copy | live notifications | slow subscribers can affect memory or delivery |
| Durable log | Consumers track offsets and replay | event history, analytics | more operational complexity and storage |

A queue normally removes a message from the ready set when it is delivered.
That is why an acknowledgement protocol is needed: a worker crash after
delivery but before acknowledgement must not silently look like success.

## Delivery and failure semantics

The teaching model uses explicit ack and nack calls:

1. publish appends to the topic's ready deque.
2. consume(topic, limit) moves up to limit records to in-flight state.
3. ack(message) permanently removes an in-flight record.
4. nack(message, requeue=True) puts it at the front for another attempt.

Requeueing at the front makes the retry visible immediately, but repeated
failures can starve later messages. A production broker usually adds attempt
counts, exponential backoff, a visibility timeout, and a dead-letter queue.
Those features also require durable state and an idempotent consumer because
at-least-once delivery can repeat work.

## Scaling decisions

Partitions allow independent consumers to process different key ranges, but
they turn global FIFO ordering into per-partition ordering. Consumer groups
share work; pub/sub subscribers each receive a copy. Choose a partition key
from the business invariant—for example, order ID when updates for one order
must remain ordered.

Keep the producer's publish acknowledgement separate from the worker's
processing acknowledgement. A durable system may confirm a write after
replication, then retry delivery after a worker failure. Exactly-once business
effects generally come from an idempotency key or transactional outbox, not
from a queue label alone.

## Worked capacity example

Assume a workload of 2,000 messages/second normally and 4,000 messages/second
at peak, with a 2 KB payload and 24-hour retention.

- Peak payload ingress = 4,000 × 2 KB = 8,000 KB/s, or about 8 MB/s.
- One day of raw payload = 8 MB/s × 86,400 s = 691,200 MB, or about 691 GB.
- Three replicas require about 691 GB × 3 = 2.07 TB before indexes, envelopes,
  filesystem overhead, and compression.
- A seven-day retention policy would require about 2.07 TB × 7 = 14.5 TB of
  replicated raw payload.

This estimate is only a storage and bandwidth starting point. Measure the
actual envelope size, compression ratio, replication factor, peak duration,
and consumer lag before choosing capacity.

## Interview prompts

- What ordering guarantee does the business actually need?
- Where do retries stop, and how is a poison message isolated?
- What makes the consumer idempotent after a timeout or duplicate delivery?
- Which data must be durable before publish returns?
- What changes when one topic reaches 10x the traffic of the others?
