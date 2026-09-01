# Runnable educational examples

These examples turn previously generated stubs into small, explicit in-memory
teaching models. Each has a focused test suite and is intended for
interview discussion: identify the invariant, walk through failure behavior,
and explain what a production design would add.

## Distributed-systems labs

- [Replicated register and quorums](04-distributed-systems/34_replicated-register-quorums.md)
  — [implementation](../../python/distributed_systems/quorum_register.py) ·
  [tests](../../tests/distributed_systems/test_quorum_register.py)
- [Consistent-hash rebalancing](04-distributed-systems/35_partitioning-and-rebalancing.md)
  — [implementation](../../python/distributed_systems/consistent_hash_ring.py) ·
  [tests](../../tests/distributed_systems/test_consistent_hash_ring.py)
- [Event-time windows](18-messaging-streaming/41_event-time-watermarks.md)
  — [implementation](../../python/distributed_systems/event_time_windows.py) ·
  [tests](../../tests/distributed_systems/test_event_time_windows.py)

These labs cover quorum intersection and read repair, bounded key movement, and
event-time finalization. They have no network, durable storage, membership
protocol, checkpointing, or concurrent execution.

## E-commerce checkout

- Implementation: [ecommerce.py](../../python/system_design/ecommerce.py)
- Tests: [test_ecommerce.py](../../tests/system_design/test_ecommerce.py)
- Contract: `checkout(user, items)` accepts a non-empty mapping of string
  product IDs to positive integer quantities. It validates the complete cart,
  reserves all requested stock atomically, and returns a confirmed immutable
  `Order` snapshot. Unknown products or insufficient stock return `None` with
  no partial reservation or order. Invalid input raises `ValueError` before
  state changes. Reserved stock can be returned through `Inventory.release`.

The example demonstrates an inventory invariant: a successful reservation
never makes available stock negative, and a failed checkout leaves the stock
ledger and order list unchanged.

## Saga orchestration

- Implementation: [saga_pattern.py](../../python/system_design/saga_pattern.py)
- Tests: [test_saga_pattern.py](../../tests/system_design/test_saga_pattern.py)
- Contract: each named `SagaStep` has a zero-argument action and compensation
  callable. `SagaOrchestrator.execute()` stops at the first action exception,
  compensates only completed steps in reverse order, and returns a
  `SagaResult` containing success, the failed step, completed steps, and
  compensation failures. Executions are reusable and do not accumulate prior
  run state.

The example intentionally reports compensation failures while continuing best-
effort cleanup, which gives an interview candidate a starting point for
discussing retries, durable state, and operator intervention.

## Search engine / inverted index

- Implementation: [search_engine.py](../../python/system_design/search_engine.py)
- Tests: [test_search_engine.py](../../tests/system_design/test_search_engine.py)
- Contract: document text and queries are case-insensitively tokenized by
  words. A query with one term returns matching document IDs; whitespace-
  separated terms are an AND query. Results preserve document insertion order,
  re-indexing is idempotent and removes stale terms, document removal deletes
  its postings, and each result is a fresh list isolated from caller changes.

The index demonstrates posting lists and intersection, but does not implement
relevance ranking or phrase search.

## Video streaming

- Implementation: [video_streaming.py](../../python/system_design/video_streaming.py)
- Tests: [test_video_streaming.py](../../tests/system_design/test_video_streaming.py)
- Contract: `Stream.upload(video_id, title)` validates non-empty strings,
  rejects duplicate IDs, and synchronously creates a ready fixed rendition
  ladder: `480p` at `1.5 Mbps`, `720p` at `3 Mbps`, and `1080p` at `6 Mbps`.
  `select_quality(video_id, bandwidth_mbps)` returns the highest sustainable
  rendition, returns `None` below `1.5 Mbps`, raises `KeyError` for an unknown
  video, and raises `ValueError` for invalid bandwidth. Returned video records
  and catalogs do not expose mutable internal state.

This is a rendition-selection exercise, not a transcoding or delivery system.
It does not model persistence, concurrency, authentication or authorization,
retries, a CDN, adaptive-bitrate segmentation, manifests, or production
capacity claims.

## News feed

- Implementation: [news_feed.py](../../python/system_design/news_feed.py)
- Tests: [test_news_feed.py](../../tests/system_design/test_news_feed.py)
- Contract: `NewsFeeder.follow(follower, author)` is idempotent and rejects
  self-following. `post(author, content)` returns an immutable, monotonically
  numbered `Post` and fans it out to the author and followers that existed at
  post time. `get_feed(user, limit=10)` returns a fresh reverse-chronological
  list. Following is prospective only; existing posts are not backfilled.

This is a small fan-out-on-write exercise. It has no persistence, concurrency
control, authentication or authorization, retries, ranking, deletion,
backfill, unfollow operation, distributed fan-out, or production capacity
claims.

## Time-series database

- Implementation: [time_series_db.py](../../python/system_design/time_series_db.py)
- Tests: [test_time_series_db.py](../../tests/system_design/test_time_series_db.py)
- Contract: `write(metric, timestamp_ms, value)` accepts a non-empty metric,
  non-negative integer timestamp, and finite numeric value. Writes may arrive
  out of order; queries sort by timestamp while preserving write order for
  equal timestamps. `query(metric, start_ms, end_ms)` uses inclusive bounds,
  returns `[]` for an unknown metric without mutating the database, and
  rejects invalid bounds.

This is an in-memory ordering and range-query exercise. It has no persistence,
concurrency control, authentication or authorization, retries, retention
automation, aggregation, downsampling, distributed coordination, or
production capacity claims.

## Message queue

- Implementation: [message_queue.py](../../python/system_design/message_queue.py)
- Tests: [test_message_queue.py](../../tests/system_design/test_message_queue.py)
- Contract: topics are explicitly created. publish returns an immutable
  monotonic message, consume(topic, limit) delivers FIFO batches into
  in-flight state, ack removes a delivered message, and nack can requeue it.

This is an in-memory acknowledgement exercise. It has no consumer groups,
visibility timeouts, persistence, partitions, concurrency control, or crash
recovery.

## Pub/Sub

- Implementation: [pub_sub_system.py](../../python/system_design/pub_sub_system.py)
- Tests: [test_pub_sub_system.py](../../tests/system_design/test_pub_sub_system.py)
- Contract: a subscription is unique per topic and subscriber ID; replacement
  preserves order, publishing broadcasts in registration order, and callback
  failures are returned while later subscribers continue receiving messages.

This model has no persistence, replay, backpressure, concurrency control,
delivery guarantee, or Redis protocol behavior.

## Circuit breaker

- Implementation: [circuit_breaker.py](../../python/system_design/circuit_breaker.py)
- Tests: [test_circuit_breaker.py](../../tests/system_design/test_circuit_breaker.py)
- Contract: consecutive failures move a breaker from CLOSED to OPEN; an
  injected clock permits one HALF_OPEN probe after the reset timeout; success
  closes it and failure reopens it. Service errors are re-raised and open
  calls raise CircuitOpenError.

This synchronous model has no concurrency coordination, sliding windows,
distributed state, or timeout enforcement.

## API gateway

- Implementation: [api_gateway.py](../../python/system_design/api_gateway.py)
- Tests: [test_api_gateway.py](../../tests/system_design/test_api_gateway.py)
- Contract: non-empty exact paths map to named callable services. Duplicate
  routes require explicit replacement; routing invokes the service, unknown
  paths raise KeyError, and service errors propagate.

This is an in-memory routing exercise with no authentication, authorization,
rate limiting, retries, load balancing, protocol translation, persistence, or
concurrency control.

## Deliberate limitations

All implementations on this page are local teaching models. They provide no:

- persistence or durable recovery;
- concurrency control or distributed coordination/fan-out;
- retries, idempotency keys, or durable workflow state;
- authentication or authorization;
- payment integration;
- production inventory/catalog guarantees;
- search ranking or full-text indexing;
- CDN delivery or adaptive-bitrate segmentation;
- retention automation;
- production capacity claims.

Use the implementations to practice invariants, APIs, and failure paths. Use
the surrounding system-design guides to discuss how these limitations would be
addressed at production scale.
