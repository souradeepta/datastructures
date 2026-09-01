# Database Systems — Study Catalog

Educational database material for interview preparation and design discussion.
The catalog is broad and unevenly reviewed: guides marked draft are not
production runbooks or guarantees. See the [documentation upgrade plan](../DOCUMENTATION_UPGRADE_PLAN.md)
for the Terra curriculum gate and the Batch-1 quality contract.

Run the standard-library audit with `python3 scripts/audit_documentation.py --summary` or
the strict first-batch profile with `python3 scripts/audit_documentation.py --profile batch-1 --fail-on-missing --summary`.

---

## 📚 Database Categories (30 Guides Total)

### Core Database Systems (10 Original Guides)

**1. 🗄️ Relational Databases (SQL)**
- **[SQL Deep Dive](01-sql-advanced.md)** — Advanced queries, optimization, transactions
- Window functions, CTEs, EXPLAIN plans, indexes, ACID

**2. 📄 Document Databases (NoSQL)**
- **[NoSQL Comprehensive Guide](02-nosql-advanced.md)** — Data modeling, consistency models, scaling
- MongoDB, DynamoDB, schema design, sharding

**3. 🔗 Graph Databases**
- **[Graph Databases](03-graph-databases.md)** — Graph queries, ACID on graphs, traversals
- Neo4j, Cypher, recommendations, fraud detection

**4. 📊 Columnar Databases**
- **[Columnar Databases](04-columnar-databases.md)** — Column families, compression, analytics
- Snowflake, BigQuery, OLAP, medallion architecture

**5. ⏱️ Time-Series Databases**
- **[Time-Series Databases](05-timeseries-databases.md)** — Bucketing, retention, downsampling
- Prometheus, InfluxDB, cardinality management

**6. 🔍 Search Engines**
- **[Search Engines & Full-Text Search](06-search-engines.md)** — Inverted indexes, ranking, aggregations
- Elasticsearch, BM25, autocomplete, faceting

**7. 💾 Cache Databases**
- **[Caching & In-Memory Stores](07-caching-stores.md)** — Eviction, persistence, clustering
- Redis, Memcached, cache patterns, leaderboards

**8. 🎯 Vector Databases**
- **[Vector Databases](08-vector-databases.md)** — Embedding search, indexing, distance metrics
- Pinecone, Weaviate, RAG, similarity search

**9. 🔀 GraphQL**
- **[GraphQL Fundamentals](09-graphql.md)** — Schema design, resolvers, N+1 problems
- Query optimization, caching strategies

**10. 🏛️ Data Warehousing & Lakehouses**
- **[Data Warehousing & Lakehouses](10-warehousing-lakehouses.md)** — Architecture, ETL, optimization
- Medallion architecture, Delta Lake, table formats

---

### Advanced Concepts (20 New Guides)

**11. 📨 Message Queues & Event Streaming**
- **[Message Queues & Event Streaming](11-message-queues-streams.md)** — Kafka, RabbitMQ, event sourcing
- Pub/Sub patterns, ordering guarantees, replay capability
- Exercises: Order processing, analytics streams, fault handling

**12. 🔄 Distributed Transactions**
- **[Distributed Transactions](12-distributed-transactions.md)** — 2PC, Sagas, consistency
- Trade-offs between blocking and eventual consistency
- Exercises: Order processing with compensations

**13. 🤝 Consensus Algorithms**
- **[Consensus Algorithms](13-consensus-algorithms.md)** — Raft, Paxos, Byzantine Fault Tolerance
- Leader election, log replication, failure recovery
- Exercises: Implement Raft node with consensus

**14. ⚖️ Load Balancing & Routing**
- **[Load Balancing & Routing](14-load-balancing-and-routing.md)** — Consistent hashing, routing strategies
- Round-robin, least-connections, geographic routing
- Exercises: Implement consistent hash ring

**15. 🔁 Database Replication & Failover**
- **[Database Replication & Failover](15-database-replication.md)** — Master-replica, multi-region
- Synchronous vs. asynchronous replication
- Exercises: Failover detection and promotion

**16. 💾 Backup & Recovery**
- **[Database Backup & Recovery](16-backup-recovery.md)** — RTO, RPO, incremental backups
- Point-in-time recovery, cross-region backup
- Exercises: Design backup strategy for scale

**17. 📋 Query Planning & Optimization**
- **[Query Planning & Optimization](17-query-planning.md)** — Cost-based optimization, statistics
- Join ordering, cardinality estimation
- Exercises: Optimize complex queries

**18. 🔑 Indexing Deep Dive**
- **[Indexing Deep Dive](18-indexing-deep-dive.md)** — B-trees, LSM trees, hash indexes
- Bitmap indexes, covering indexes
- Exercises: Choose optimal index structure

**19. 📍 Sharding Strategies Deep Dive**
- **[Sharding Strategies Deep Dive](19-sharding-advanced.md)** — Range, hash, directory-based
- Consistent hashing, rebalancing, hotspot detection
- Exercises: Design sharding for scale-out

**20. 📤 Change Data Capture (CDC)**
- **[Change Data Capture](20-change-data-capture.md)** — Log-based, query-based CDC
- Streaming changes to downstream systems
- Exercises: Implement CDC pipeline

**21. 🔄 Eventual Consistency Patterns**
- **[Eventual Consistency Patterns](21-eventual-consistency.md)** — Read-your-write, monotonic reads
- Handling stale reads, conflict resolution
- Exercises: Design eventual consistency system

**22. 🔍 Distributed Tracing & Observability**
- **[Distributed Tracing](22-distributed-tracing.md)** — Span tracking, latency analysis
- Sampling, correlation IDs, flame graphs
- Exercises: Trace production incident

**23. 📑 API Pagination & Filtering**
- **[API Pagination & Filtering](23-api-pagination.md)** — Cursor-based, offset-based pagination
- Filter syntax, sorting strategies
- Exercises: Implement efficient pagination

**24. 📊 Database Monitoring & Alerting**
- **[Database Monitoring & Alerting](24-database-monitoring.md)** — Key metrics, anomaly detection
- Query latency, connection pools, disk usage
- Exercises: Design monitoring dashboard

**25. 🔌 Connection Pooling**
- **[Connection Pooling](25-connection-pooling.md)** — Pool sizing, idle timeout, queue management
- Connection lifecycle, resource limits
- Exercises: Implement connection pool

**26. 🔀 Database Migration Strategies**
- **[Database Migration Strategies](26-migration-strategies.md)** — Zero-downtime migration, dual writes
- Shadow traffic, feature flags, rollback
- Exercises: Plan major schema migration

**27. 👥 Multi-tenancy Patterns**
- **[Multi-tenancy Patterns](27-multi-tenancy.md)** — Shared database, schema-per-tenant, database-per-tenant
- Row-level security, data isolation
- Exercises: Design multi-tenant architecture

**28. 🔒 Database Security & Encryption**
- **[Database Security](28-database-security.md)** — Encryption at rest, in-transit, TDE
- Access control, audit logging, compliance
- Exercises: Implement encryption strategy

**29. ⚡ Time-Series Optimization Deep Dive**
- **[Time-Series Optimization](29-time-series-optimization.md)** — Specialized compression, retention
- Downsampling, aggregate tables, tiered storage
- Exercises: Optimize a high-volume metrics workload

**30. 🌊 Stream Processing & Complex Event Processing**
- **[Stream Processing](30-stream-processing.md)** — Kafka Streams, Flink, window operations
- Stateful processing, joins, aggregations
- Exercises: Implement real-time analytics

---

## 🎯 Database Selection Guide

| Use Case | Best Option | Runner-Up | Why |
|----------|------------|-----------|-----|
| **Transactional** | PostgreSQL | MySQL | ACID, complex queries, relationships |
| **Flexible documents** | MongoDB | Firebase | Schema flexibility, scale-out, embedded data |
| **Large key-value workload** | DynamoDB | Cassandra | Partition-key access and managed horizontal scaling; validate limits and cost for the workload |
| **Analytics** | Snowflake | BigQuery | Columnar compression, separation of compute/storage |
| **Search** | Elasticsearch | Meilisearch | Inverted indexes, complex ranking, BM25 |
| **Graphs/relationships** | Neo4j | ArangoDB | Relationship traversals, pattern matching |
| **Time-series metrics** | Prometheus | InfluxDB | Bucketization, downsampling, retention |
| **Caching** | Redis | Memcached | Data structures, persistence, pub/sub |
| **Semantic search** | Pinecone | Weaviate | Vector indexing, HNSW algorithms |
| **APIs** | GraphQL | REST | Client-driven queries, strongly typed |

---

## 🔀 Comprehensive Comparison Matrix

### Qualitative workload trade-offs

The table below is a selection aid, not a benchmark or a universal guarantee.
Throughput, latency, practical scale, and consistency depend on data shape,
query/index choices, region, instance or service tier, and provider/version;
measure a representative workload before capacity planning.

| Model | Typical strength | Main boundary to investigate | Consistency/freshness question |
|---|---|---|---|
| PostgreSQL/MySQL | Relational constraints, joins, and transactions | Write contention, index cost, and vertical/replica limits | What isolation and replica-read behavior is required? |
| MongoDB/DynamoDB/Cassandra | Access-pattern-driven document or key-value scale-out | Partition-key skew, item/document limits, and cross-record queries | Which reads may be stale, and which writes need conditions? |
| Elasticsearch | Text search, ranking, and faceting | Refresh lag, shard sizing, and indexing cost | How stale may search results be? |
| Redis/Memcached | Low-overhead cache and ephemeral coordination patterns | Memory cost, eviction, failover, and durability needs | Is loss or stale data acceptable for this key? |
| Neo4j/Neptune/ArangoDB | Multi-hop relationship traversal | Supernodes, traversal bounds, and cross-partition paths | Which edges must reflect revocation immediately? |
| Snowflake/BigQuery | Elastic analytical scans and aggregates | Scan cost, queueing, and transformation freshness | What is the acceptable batch/streaming delay? |
| Prometheus/InfluxDB | Time-windowed metrics and retention policies | Series cardinality, retention, and remote-write behavior | How much historical data must be queryable? |
| Pinecone/Weaviate/Milvus | Approximate or exact vector retrieval | Recall/latency trade-off, filtering, and embedding version | When may index/model updates become visible? |

---

### Data Model Fit

```
                    ┌─────────────────────────────────┐
                    │    Data Model Comparison        │
                    └─────────────────────────────────┘

Tabular Data (Rows/Columns)
├─ PostgreSQL (Normalized, ACID)
├─ MySQL (Transactional)
└─ Snowflake (Denormalized for analytics)

Document Data (JSON-like)
├─ MongoDB (Flexible schema)
├─ Firebase (Real-time)
└─ DynamoDB (Key-value with attributes)

Graph Data (Nodes/Relationships)
├─ Neo4j (Property graphs)
├─ ArangoDB (Multi-model)
└─ Amazon Neptune (Managed)

Time-Series Data (Timestamps)
├─ Prometheus (Metrics)
├─ InfluxDB (Time-bucketed)
├─ TimescaleDB (PostgreSQL extension)
└─ VictoriaMetrics (Efficient)

Vector Data (Embeddings)
├─ Pinecone (Specialized)
├─ Weaviate (Open-source)
├─ Milvus (Cloud-native)
└─ Qdrant (Rust-based)

Full-Text Search (Inverted Indexes)
├─ Elasticsearch (Feature-rich)
├─ Solr (Apache)
├─ Meilisearch (Simple)
└─ Algolia (Managed)

Key-Value Cache (In-Memory)
├─ Redis (Rich data structures)
├─ Memcached (Simple)
└─ Dragonfly (Redis-compatible)
```

---

### Cost vs. Performance Trade-off

```
Cost
 ↑
 │          Snowflake
 │           (expensive,
 │         scalable)
 │                    ┌─ BigQuery (pay per query)
 │          PostgreSQL │
 │          (moderate)  │
 │         ┌────────────┤
 │        ╱             └─ DynamoDB (pay per op)
 │       ╱ MongoDB
 │      ╱  (moderate)
 │     ╱   ┌──────────────
 │    ╱    │
 │   ╱     ├─ Elasticsearch
 │  ╱      │  (self-hosted, cheap)
 │ ╱       │
 │╱        ├─ Redis (in-memory)
 │         │
 └─────────┴─────────────────────→
           Performance/Scale
```

---

### Consistency vs. Availability (CAP Theorem)

```
        ┌─────────────────────────────┐
        │   CAP Theorem Choices       │
        └─────────────────────────────┘

Choose 2 of 3:
- Consistency (C): All reads see latest write
- Availability (A): System always responsive
- Partition tolerance (P): Survives network splits

Consistency + Partition (CP):
├─ PostgreSQL (strong consistency)
├─ Neo4j (single region)
└─ MongoDB (single datacenter)

Availability + Partition (AP):
├─ DynamoDB (eventual consistency mode)
├─ Cassandra (eventual)
└─ Elasticsearch (eventually consistent)

Consistency + Availability (CA):
├─ Not possible in distributed systems
└─ Single-region deployments approach this
```

---

## 🏗️ Architecture Patterns

### Single Database
```
App → PostgreSQL
      (Simple, limited scale)
```

### Master-Replica
```
Write ──→ Primary ────→ Read Replicas
         PostgreSQL    (Read-only)
                      Async replication
```

### Sharding
```
Shard 0: user_id % 3 = 0
Shard 1: user_id % 3 = 1  
Shard 2: user_id % 3 = 2

App → Router → [Shard0, Shard1, Shard2]
      (Consistent hash or range-based)
```

### CQRS (Command-Query Responsibility Segregation)
```
Write → DynamoDB (optimized for writes)
Read  → Elasticsearch (optimized for reads)
        (Background sync)
```

### Cache-Aside Pattern
```
Request ──→ Cache (Redis)?
            ├─ Hit: Return
            └─ Miss: Query DB, store in cache
```

---

## 📊 Interview Path

### Beginner (Week 1)
1. SQL basics (indexes, joins, transactions)
2. NoSQL vs. SQL (when use each)
3. Database selection for scenario

### Intermediate (Weeks 2-3)
4. Advanced SQL (window functions, CTEs, optimization)
5. MongoDB data modeling
6. Caching strategy (Redis)
7. Elasticsearch basics

### Advanced (Weeks 4+)
8. System design: pick a database for a stated user/event workload
9. Distributed databases (Cassandra, DynamoDB)
10. Time-series, vector databases
11. GraphQL API design

---

## 🔑 Key Concepts by Database Type

### Relational (SQL)
- **Normalization:** Minimize redundancy
- **ACID:** Transactions
- **Indexes:** Fast queries
- **Joins:** Combine tables

### Document (NoSQL)
- **Schema flexibility:** Evolve over time
- **Sharding:** Horizontal scaling
- **Replication:** High availability
- **Eventual consistency:** Trade-off for scale

### Graph
- **Nodes & edges:** Relationship representation
- **Graph algorithms:** Shortest path, PageRank
- **Pattern matching:** Complex queries
- **Traversals:** Navigate relationships

### Columnar
- **Compression:** Similar data together
- **Aggregations:** Fast SUM, AVG, COUNT
- **Partitioning:** Organize by time/region
- **OLAP:** Analytics queries

### Time-Series
- **Time bucketing:** Group by interval
- **Downsampling:** Aggregate old data
- **Retention:** Delete old data automatically
- **Cardinality:** Label combinations

---

## 💡 Common Interview Questions

**Q: Design a database for a stated user/event workload**
→ State traffic, retention, access patterns, and freshness first; then compare
SQL, NoSQL, and analytical projections against those assumptions

**Q: Real-time feed for a high-volume event stream**
→ NoSQL (MongoDB/DynamoDB) with caching (Redis)

**Q: Social network with friend recommendations**
→ Graph database (Neo4j) for relationships, recommendations

**Q: Monitoring system for a fleet of servers**
→ Time-series DB (Prometheus) for metrics, Elasticsearch for logs

**Q: E-commerce product search**
→ Elasticsearch for search, SQL for transactions

---

## 🧪 Hands-On Practice

### SQL
- 10+ complex queries (window functions, CTEs)
- Index optimization
- Transaction isolation levels

### NoSQL
- MongoDB aggregation pipeline
- DynamoDB access patterns
- Sharding strategy

### Advanced
- Design database schema for real system
- Query optimization with EXPLAIN plans
- Caching strategy for hot data

---

## 📚 Resources by Topic

| Topic | Guide | Difficulty |
|-------|-------|-----------|
| SQL basics | 01-sql-advanced.md | Medium |
| NoSQL modeling | 02-nosql-advanced.md | Medium-Hard |
| Graphs | 03-graph-databases.md | Hard |
| Analytics | 04-columnar-databases.md | Medium |
| Metrics | 05-timeseries-databases.md | Medium |
| Search | 06-search-engines.md | Medium |
| Caching | 07-caching-stores.md | Medium |
| Embeddings | 08-vector-databases.md | Hard |
| APIs | 09-graphql.md | Medium |
| Warehousing | 10-warehousing-lakehouses.md | Hard |

---

## ✅ Self-Assessment

By the end of this section, you should be able to:

- [ ] Explain SQL vs. NoSQL trade-offs
- [ ] Design database schema for given requirements
- [ ] Write complex SQL queries (joins, aggregations, window functions)
- [ ] Explain MongoDB data modeling and indexing
- [ ] Design a sharding strategy for a large table and stated access patterns
- [ ] Explain graph database use cases
- [ ] Design caching strategy (Redis)
- [ ] Understand Elasticsearch basics
- [ ] Explain GraphQL schema design
- [ ] Pick right database for scenario

---

**Last updated:** 2026-08-31

**Catalog:** 30 database guides, plus this navigation page and the interview question bank
**Batch 1:** 8 foundational guides are reviewed with Terra gate: approved; maintainer confirmation remains open
**Coverage:** Relational, NoSQL, graphs, columnar, time-series, search, caching, vectors, GraphQL, warehousing, and distributed data systems
