# System-design content status

The system-design directory is a broad study catalog, not a uniformly reviewed
set of production designs. It currently contains 705 active topic-guide Markdown
files in 19 topic directories. The count excludes landing pages, status/index
pages, and nested README pages.

## Status definitions

- **Tested**: the repository contains a focused automated test for the linked
  implementation. Tests validate the educational API; they do not prove that a
  design is production-ready.
- **Reviewed**: a maintainer has manually checked the guide’s objective,
  architecture, calculations, trade-offs, failure modes, and links.
- **Draft**: content is useful for exploration but has not passed the reviewed
  standard. Draft content may contain incomplete examples or calculations.

## Currently verified examples

These are the twenty system-design test groups with focused tests in the
repository. They are **tested**, but this is not a claim that the entire catalog
is reviewed:

- [LRU cache implementation](../../python/system_design/lru_cache.py) — [tests](../../tests/system_design/test_lru_cache.py)
- [LFU cache implementation](../../python/system_design/lfu_cache.py) — [tests](../../tests/system_design/test_lfu_cache.py)
- [Rate limiter implementation](../../python/system_design/rate_limiter.py) — [tests](../../tests/system_design/test_rate_limiter.py)
- [URL shortener implementation](../../python/system_design/url_shortener.py) — [tests](../../tests/system_design/test_url_shortener.py)
- [Parking lot implementation](../../python/system_design/parking_lot.py) — [tests](../../tests/system_design/test_parking_lot.py)
- [Load balancer implementation](../../python/system_design/load_balancer.py) — [tests](../../tests/system_design/test_load_balancer.py)
- [Design-pattern implementations](../../python/system_design/adapter_pattern.py) — [focused tests](../../tests/system_design/test_design_pattern_examples.py)
- [E-commerce checkout](../../python/system_design/ecommerce.py) — [tests](../../tests/system_design/test_ecommerce.py)
- [Saga orchestration](../../python/system_design/saga_pattern.py) — [tests](../../tests/system_design/test_saga_pattern.py)
- [Search engine / inverted index](../../python/system_design/search_engine.py) — [tests](../../tests/system_design/test_search_engine.py)
- [Video streaming](../../python/system_design/video_streaming.py) — [tests](../../tests/system_design/test_video_streaming.py)
- [News feed](../../python/system_design/news_feed.py) — [tests](../../tests/system_design/test_news_feed.py)
- [Time-series database](../../python/system_design/time_series_db.py) — [tests](../../tests/system_design/test_time_series_db.py)
- [Message queue](../../python/system_design/message_queue.py) — [tests](../../tests/system_design/test_message_queue.py)
- [Pub/Sub](../../python/system_design/pub_sub_system.py) — [tests](../../tests/system_design/test_pub_sub_system.py)
- [Circuit breaker](../../python/system_design/circuit_breaker.py) — [tests](../../tests/system_design/test_circuit_breaker.py)
- [API gateway](../../python/system_design/api_gateway.py) — [tests](../../tests/system_design/test_api_gateway.py)
- [Replicated quorum register](../../python/distributed_systems/quorum_register.py) — [tests](../../tests/distributed_systems/test_quorum_register.py)
- [Consistent-hash ring](../../python/distributed_systems/consistent_hash_ring.py) — [tests](../../tests/distributed_systems/test_consistent_hash_ring.py)
- [Event-time windows](../../python/distributed_systems/event_time_windows.py) — [tests](../../tests/distributed_systems/test_event_time_windows.py)

The [runnable educational examples guide](EDUCATIONAL_EXAMPLES.md) defines the
contracts and limitations for these twenty in-memory models. They are runnable
practice, not production systems.

No broader reviewed set is claimed until individual guides receive the manual
review described above. Other implementations and guides should be treated as
draft or illustrative unless their status is explicitly documented.

## Known content debt baseline

The audit baseline currently tracks:

- **27 structural-filler guides**, all in `16-networking/`, containing generic
  sections such as “Primary element,” “Advantage 1,” and “Use case 1.”
- **134 copied-capacity guides**, containing the shared `100M users` / `474
  MB/s` sizing block. The block includes a known unit error: 474 MB/s is about
  3.8 Gbps, not 3.8 Tbps.

These counts are a regression boundary, not an endorsement of the content. The
active audit reports affected paths by topic and fails CI only when a count
increases beyond its approved threshold. Archived material is outside this
routine audit.

## Reader warning

Do not use unreviewed capacity estimates, availability claims, or architecture
choices as production guidance. Recalculate numbers for the stated workload,
check units, and discuss consistency, failure recovery, security, and cost.
Use the tested examples above for runnable practice while the wider catalog is
being reviewed and rewritten.
