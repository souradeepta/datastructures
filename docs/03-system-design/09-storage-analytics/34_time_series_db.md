# Time Series Database

**Status:** draft
**Audience:** Data/platform engineer preparing for an L4–L5 metrics-storage interview.
**Prerequisites:** time-series cardinality, WALs, compaction, retention, rollups, and query windows.
**Sequence:** Batch 5, storage-analytics debt follow-on
**Terra gate:** open

## Problem Statement
Design a database optimized for time-indexed data (metrics, logs, events).

**Requirements:**
- Fast ingestion (millions per second)
- Efficient storage (compression)
- Time range queries
- Aggregation (sum, avg, count)


## Code Explanation (Detailed)

### Sharding Key Selection
Hash-based: shard_id = hash(key) % num_shards
- Even distribution (no hot shards from skew)
- Consistent hashing minimizes resharding

### Query Routing
1. Compute shard_id from key
2. Route to master (write) or replica (read)
3. Async replication to other replicas

### Handling Hot Shards
1. Detect via monitoring (QPS per shard)
2. Solutions:
   - Add more replicas (read scaling)
   - Cache hot keys locally (in-process)
   - Split shard (expensive but permanent)

### Resharding Data
1. Dual-write: write to old and new
2. Migrate: copy data to new shards
3. Verify: checksums match
4. Switch: route to new
5. Cleanup: remove old shards

## Design

### Data Layout

```
By time: Column-oriented storage
Sequential writes: Efficient ingestion
Compression: Gorilla algorithm (70% reduction)
Indexing: Block index for range queries
```

### Retention Policy

```
Hot data: Recent data (30 days) in fast storage
Warm data: Older (30-365 days) in slower
Cold data: Archive data (1+ years)
Automatic downsampling: Hourly from daily
```

### Querying

```
Time range: Efficient range scans
Aggregation: Push-down to storage
Downsampling: Return coarser resolution
Distributed: Parallel across shards
```


## Scenario

Time Series Database is a critical component in modern distributed systems. In real-world applications, persisting and querying structured data at scale. For example, major tech companies like Netflix, Uber, and Airbnb rely on similar solutions to handle millions of concurrent users and requests. The challenge is achieving this while maintaining sub-100ms latency, 99.99% availability, and gracefully handling 10x traffic spikes during peak demand. This component provides the foundational capability to solve these challenges reliably and efficiently at global scale.

## Users

- **Backend Engineers**: Responsible for implementing and maintaining this system component in production environments. They need to understand the architecture, trade-offs, failure modes, and operational considerations.
- **DevOps/SRE Teams**: Monitor system health, manage scaling policies, handle incidents, and ensure reliability SLAs are met. They need insights into performance characteristics, bottlenecks, and failure recovery mechanisms.
- **Data Engineers**: Design data pipelines and analytics around this system, requiring deep understanding of data flow, consistency guarantees, and throughput characteristics.
- **System Architects**: Make high-level architectural decisions that impact company infrastructure, requiring comprehensive understanding of capabilities, limitations, and scalability boundaries.
- **Security Teams**: Understand security implications, potential vulnerabilities, and compliance requirements for this component.

## PRD

### Functional Requirements
- Partition data across multiple shards
- Route queries to correct shard
- Replicate within each shard
- Support resharding (add/remove shards)
- Cross-shard scatter-gather queries

### Non-Functional Requirements
- Scalability: 100+ shards, petabyte scale
- Availability: 99.99%, auto-failover
- Latency: < 100ms single-shard, < 500ms cross-shard
- Consistency: strong within shard, eventual across shards
- Operational simplicity: auto-rebalance, monitoring

### Success Metrics
- Even data distribution (< 10% skew)
- Even traffic distribution (< 10% skew)
- Resharding in < 1 hour
- Query routing overhead < 1ms


## Flow

The typical operational flow for this system involves these key phases:

1. **Request Arrival**: Client/upstream system sends request with required parameters and context
2. **Validation & Routing**: System validates request format, authentication, and routes to correct handler/shard/instance
3. **Core Processing**: Execute the main algorithm, database query, or business logic on the data/state
4. **State Management**: Update internal state (caches, indexes, counters, logs) with proper atomicity and locking
5. **Response Generation**: Format results and return to requester with relevant metadata (timing, version info)
6. **Observability**: Record metrics (latency, throughput, errors), logs (for debugging), and traces (for performance analysis)

This flow repeats thousands or millions of times per second in production. Each operation's efficiency compounds across the entire system, making careful optimization essential. Bottlenecks at any phase can cascade to impact overall system performance.

## Architecture Diagram

```
┌───────────────────────────────┐
│   Time Series Data Storage   │
│  Ingestion (InfluxDB)         │
│  - Write-optimized            │
│  - Append-only, no updates    │
│  Compression                  │
│  - Delta-of-delta encoding    │
│  - XOR float (8x savings)     │
│  Querying                     │
│  - Range queries O(log n)     │
│  - Aggregations (SUM, AVG)    │
│  - Downsampled data           │
└───────────────────────────────┘
```

## Back-of-Envelope Calculations

1M servers, 1K metrics/server, 1 sample/min. Ingestion: 1B metrics/min. Storage: 8GB/min raw, 1GB/min compressed = 400TB/month.
## Design Choice Comparison

| Approach | Pros | Cons |
|----------|------|------|
| General DB | Flexible | Poor compression |
| TSDB | Optimized | Less flexible |
| Data warehouse | Analytics | Slower |

## Follow-up Interview Questions

1. Query across timezones? 2. Real-time alerts? 3. Out-of-order writes? 4. Ingestion bottleneck? 5. Cold storage migration?

## Example Scenario Walkthrough

[Describe a concrete example with step-by-step execution]

### Architecture Diagram

```mermaid
graph TB
    Metrics["Metrics"]
    Ingestion["Ingestion Service"]
    Storage["Time Series DB"]
    Query["Query Engine"]
    Visualization["Visualization"]

    Metrics -->|Stream| Ingestion
    Ingestion -->|Store| Storage
    Query -->|Read| Storage
    Query -->|Render| Visualization
```

### Flow Diagram

```mermaid
flowchart TD
    A["Metric arrives"] --> B["Timestamp"]
    B --> C["Tags"]
    C --> D["Value"]
    D --> E["Compress"]
    E --> F["Store Block"]
    F --> G["Index"]
```

## Complexity

| Operation | Time |
|-----------|------|
| Write | O(1) |
| Range query | O(log n + k) |
| Aggregation | O(k) |

## Python Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import bisect

@dataclass
class DataPoint:
    timestamp: int  # Unix ms
    value: float
    tags: Dict[str, str] = field(default_factory=dict)

class TimeSeries:
    def __init__(self, name: str):
        self.name = name
        self._timestamps: List[int] = []
        self._values: List[float] = []

    def write(self, ts: int, value: float):
        idx = bisect.bisect_left(self._timestamps, ts)
        self._timestamps.insert(idx, ts)
        self._values.insert(idx, value)

    def query(self, start: int, end: int) -> List[Tuple[int, float]]:
        lo = bisect.bisect_left(self._timestamps, start)
        hi = bisect.bisect_right(self._timestamps, end)
        return list(zip(self._timestamps[lo:hi], self._values[lo:hi]))

    def aggregate(self, start: int, end: int, fn: str = "avg") -> Optional[float]:
        points = [v for _, v in self.query(start, end)]
        if not points:
            return None
        if fn == "avg": return sum(points) / len(points)
        if fn == "sum": return sum(points)
        if fn == "max": return max(points)
        if fn == "min": return min(points)
        return None

class TimeSeriesDB:
    def __init__(self):
        self._series: Dict[str, TimeSeries] = {}

    def write(self, metric: str, ts: int, value: float):
        if metric not in self._series:
            self._series[metric] = TimeSeries(metric)
        self._series[metric].write(ts, value)

    def query(self, metric: str, start: int, end: int) -> List[Tuple[int, float]]:
        return self._series.get(metric, TimeSeries(metric)).query(start, end)

# Usage
db = TimeSeriesDB()
for i, v in enumerate([12.5, 13.0, 11.8, 14.2]):
    db.write("cpu.usage", 1000 + i * 1000, v)
print(db.query("cpu.usage", 1000, 4000))
```

## Java Implementation

```java
import java.util.*;

public class TimeSeriesDB {
    private Map<String, TreeMap<Long, Double>> series = new HashMap<>();

    public void write(String metric, long timestamp, double value) {
        series.computeIfAbsent(metric, k -> new TreeMap<>()).put(timestamp, value);
    }

    public NavigableMap<Long, Double> query(String metric, long start, long end) {
        TreeMap<Long, Double> ts = series.getOrDefault(metric, new TreeMap<>());
        return ts.subMap(start, true, end, true);
    }

    public OptionalDouble aggregate(String metric, long start, long end, String fn) {
        Collection<Double> values = query(metric, start, end).values();
        return switch (fn) {
            case "avg" -> values.stream().mapToDouble(d -> d).average();
            case "max" -> values.stream().mapToDouble(d -> d).max();
            case "min" -> values.stream().mapToDouble(d -> d).min();
            default -> OptionalDouble.empty();
        };
    }
}
```

## Common Questions & Answers

**Q: What is database sharding and why do we need it?**

A: Sharding distributes data across multiple databases to scale horizontally beyond single-machine limits. Each shard holds subset of data. Enables serving more throughput and storing larger datasets. Trade-off: querying across shards is harder.

**Q: What are common sharding strategies?**

A: Range-based (user_id: 1-1M, 1M-2M, etc.), hash-based (hash(key) % num_shards), directory-based (lookup table), geographic (shard by region). Choose based on query patterns and data distribution.

**Q: What is the hot shard problem?**

A: One shard receives much more traffic/data than others due to skewed distribution (e.g., all new users in same range). Becomes bottleneck. Solution: split hot shard, use better sharding key, or combine with caching.

**Q: How do you route queries to correct shard?**

A: Middleware computes shard_id = hash(key) % num_shards or range lookup. Routes request to correct database. Must be consistent: same key always routes to same shard. Client or proxy layer handles routing.

**Q: What happens when you add a new shard?**

A: Data must be re-distributed. Existing shards reshare (redistribute their data). Causes temporary downtime and data movement overhead. Use consistent hashing to minimize data movement.

**Q: Can you join data across shards?**

A: Very difficult. Requires querying multiple shards and joining in application code (slow). Solution: denormalize (store denormalized copies), use distributed query engine (Presto), or redesign schema.

**Q: How do you handle transactions across shards?**

A: Distributed transactions (2-phase commit) are slow and risky. Prefer: single-shard transactions (common case), saga pattern (multi-step local transactions), or eventual consistency (async coordination).

**Q: How do you choose sharding key?**

A: Key used to determine shard. Must have good cardinality (many unique values) and distribute evenly. Avoid sharding by frequently queried field (makes range queries hard). Common: user_id (for user-centric), timestamp (for time-series).

**Q: What is consistent hashing and when to use it?**

A: Hash-based sharding that minimizes data movement on shard count changes. When you add/remove shard, only ~1/n data moves (not all). Distributed systems standard (Dynamo, Cassandra, consistent caching).

**Q: How do you monitor shard health and skew?**

A: Track data size per shard, QPS per shard, latency per shard. Alert on skew (some shards much larger/busier). Manually or auto-rebalance when detected.

## Follow-up Questions & Answers

**Q: How would you implement geo-distributed sharding?**

A: Shard by geographic region (US, EU, APAC). Each region has replicas across data centers. Route based on user location. Handle eventual consistency between regions (strong eventual consistency).

**Q: How do you prevent hot keys within a shard?**

A: Detect hot keys (some keys far more accessed). Create micro-shards for hot keys (hash(key, counter) for replicas). Use caching layer above database. Monitor continuously.

**Q: What is the trade-off between range sharding and hash sharding?**

A: Range: enables range queries easily but may create hot shards (recent data). Hash: distributes evenly but makes range queries require scatter-gather. Choose based on query patterns.

**Q: How would you re-shard with minimal downtime?**

A: Dual-write strategy: write to both old and new shard layouts simultaneously. Gradually migrate data. Verify consistency. Switch reads to new layout. Clean up old shards.

**Q: Can you shard by multiple columns (composite key)?**

A: Yes, use (col1, col2) as shard key. Example: (user_id, tenant_id). Better distribution but more complex routing. Worth it for multi-tenant systems.

**Q: How do you handle shard failures?**

A: Use replication within each shard (master-slave). Detect failure, promote replica. Use consensus (Raft) for automatic failover. Trade: replication cost vs. availability.

**Q: How would you implement resharding without data movement (virtual sharding)?**

A: Map logical shards to physical shards via lookup table. When resharding, update mapping (no data movement). Trade: lookup overhead vs. seamless resharding.

**Q: How do you implement cross-shard aggregations?**

A: Scatter query to all shards. Gather results. Aggregate (sum, avg, max). Example: COUNT(*) requires hitting all shards. Slow but necessary for global analytics.

**Q: Can you migrate from single database to sharded?**

A: Yes, gradually. Start with logical sharding (single physical DB). Add more physical shards incrementally. Dual-write during migration. Atomic switch after validation.

**Q: How do you handle uneven shard growth?**

A: Monitor size growth. Split large shards before they get too big. Use growth-aware splitting (split at median timestamp for time-series). Automate with monitoring tools.


## System Overview

**Scale Metrics:**
- Throughput: Millions of operations per second
- Latency: Sub-millisecond to sub-second response times
- Data volume: Gigabytes to Petabytes
- Concurrent users: Millions to billions
- Availability: 99.99% to 99.999% uptime SLA

**Key Components:**
- Request handling and routing
- Data processing and storage
- Replication and consistency
- Failure detection and recovery
- Monitoring and alerting

## Architecture Diagrams

### System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        C1["Client"]
        LB["Load Balancer"]
    end

    subgraph "Service Layer"
        S1["Service 1"]
        S2["Service 2"]
        S3["Service N"]
    end

    subgraph "Cache"
        CACHE["Redis/Memcached"]
    end

    subgraph "Storage"
        DB["Primary DB"]
        REP["Replicas"]
    end

    C1 --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    S1 --> CACHE
    S2 --> CACHE
    S3 --> CACHE
    CACHE --> DB
    DB --> REP

    style C1 fill:#e1f5ff
    style S1 fill:#f3e5f5
    style CACHE fill:#fff3e0
    style DB fill:#e8f5e9
```

### Data Flow

```mermaid
graph LR
    A["Request"] --> B["Parse"]
    B --> C["Validate"]
    C --> D["Process"]
    D --> E["Cache"]
    E --> F["Store"]
    F --> G["Response"]

    style A fill:#c8e6c9
    style B fill:#ffccbc
    style C fill:#bbdefb
    style D fill:#f8bbd0
    style E fill:#ffe0b2
    style F fill:#d1c4e9
    style G fill:#c8e6c9
```

### Failover Mechanism

```mermaid
graph TB
    A["Primary Node"] -->|heartbeat| B["Health Checker"]
    C["Replica 1"] -->|heartbeat| B
    D["Replica 2"] -->|heartbeat| B
    B -->|failure detected| E["Coordinator"]
    E -->|elect new primary| F["New Primary"]
    F -->|start accepting| G["Clients"]

    style A fill:#ffcdd2
    style F fill:#c8e6c9
    style G fill:#fff9c4
```

### Consistency Models

```mermaid
graph TB
    subgraph "Strong Consistency"
        A1["Quorum Write"] --> A2["Read Latest"]
    end

    subgraph "Eventual Consistency"
        B1["Write Async"] --> B2["Replicate"]
        B2 --> B3["Read May Stale"]
    end

    subgraph "Causal Consistency"
        C1["Track Causality"] --> C2["Enforce Order"]
    end

    style A1 fill:#c8e6c9
    style B1 fill:#ffccbc
    style C1 fill:#bbdefb
```

### Scaling Strategy

```mermaid
graph TB
    subgraph "Vertical Scaling"
        V1["Bigger CPU"] --> V2["More RAM"]
        V2 --> V3["Faster Disk"]
    end

    subgraph "Horizontal Scaling"
        H1["Add Replicas"] --> H2["Shard Data"]
        H2 --> H3["Distributed Cache"]
    end

    subgraph "Result"
        R["Increased Capacity"]
    end

    V3 --> R
    H3 --> R

    style V1 fill:#bbdefb
    style H1 fill:#f8bbd0
    style R fill:#c8e6c9
```

## Implementation Examples

### Python Implementation

```python
# Python Implementation

from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration for the system."""
    timeout_ms: int = 5000
    retry_count: int = 3
    batch_size: int = 100
    max_connections: int = 1000

class Handler:
    """Main handler class for operations."""

    def __init__(self, config: Config):
        self.config = config
        self.metrics = {"success": 0, "failure": 0, "latency_ms": []}

    async def process(self, data: Any) -> Any:
        """Process request with error handling."""
        try:
            # Validate input
            self._validate(data)

            # Execute operation
            result = await self._execute(data)

            # Track metrics
            self.metrics["success"] += 1
            return result

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            self.metrics["failure"] += 1
            raise

    def _validate(self, data: Any) -> None:
        """Validate input data."""
        if data is None:
            raise ValueError("Data cannot be None")

    async def _execute(self, data: Any) -> Any:
        """Execute core logic."""
        # Implement actual logic here
        return {"status": "success", "timestamp": datetime.now().isoformat()}

    def get_metrics(self) -> dict:
        """Return collected metrics."""
        return self.metrics

# Usage example
async def main():
    config = Config(timeout_ms=5000, batch_size=100)
    handler = Handler(config)
    result = await handler.process({"key": "value"})
    print(f"Result: {result}")
    print(f"Metrics: {handler.get_metrics()}")
```

### Java Implementation

```java
// Java Implementation

import java.util.*;
import java.util.concurrent.*;
import java.time.Instant;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SystemHandler {
    private static final Logger logger = LoggerFactory.getLogger(SystemHandler.class);

    private final Config config;
    private final Map<String, Long> metrics = new ConcurrentHashMap<>();
    private final ExecutorService executor;

    public static class Config {
        public int timeoutMs = 5000;
        public int retryCount = 3;
        public int batchSize = 100;
        public int maxConnections = 1000;

        public Config withTimeoutMs(int timeout) {
            this.timeoutMs = timeout;
            return this;
        }
    }

    public SystemHandler(Config config) {
        this.config = config;
        this.executor = Executors.newFixedThreadPool(
            Math.min(config.maxConnections, 10)
        );
        metrics.put("success", 0L);
        metrics.put("failure", 0L);
    }

    public <T> T process(Object data) throws Exception {
        try {
            // Validate input
            validate(data);

            // Execute operation
            Object result = execute(data);

            // Track metrics
            metrics.put("success", metrics.get("success") + 1);
            return (T) result;

        } catch (Exception e) {
            logger.error("Processing failed: {}", e.getMessage());
            metrics.put("failure", metrics.get("failure") + 1);
            throw e;
        }
    }

    private void validate(Object data) throws IllegalArgumentException {
        if (data == null) {
            throw new IllegalArgumentException("Data cannot be null");
        }
    }

    private Object execute(Object data) throws Exception {
        // Implement core logic
        return Map.of(
            "status", "success",
            "timestamp", Instant.now().toString()
        );
    }

    public Map<String, Long> getMetrics() {
        return new HashMap<>(metrics);
    }

    public void shutdown() {
        executor.shutdown();
    }

    public static void main(String[] args) throws Exception {
        Config config = new Config()
            .withTimeoutMs(5000);

        SystemHandler handler = new SystemHandler(config);
        Object result = handler.process(Map.of("key", "value"));
        System.out.println("Result: " + result);
        System.out.println("Metrics: " + handler.getMetrics());
        handler.shutdown();
    }
}
```

## Back-of-Envelope Calculations

### Traffic & Throughput
**Assumptions:**
- Daily active users: 100 million (100M)
- Requests per user per day: 50
- Peak hour traffic: 10% of daily (concentrated)
- Request distribution: 70% read, 30% write

**Calculations:**
```
Assume 200,000 active series sampled every 15 seconds. Ingest is `200,000 / 15 ≈ 13,333 samples/s`; at 2 compressed bytes/sample, seven-day sample storage is about 16.1 GB before WAL, labels, indexes, replicas, and compaction overhead.
Average RPS = 5B requests / 86400 seconds ≈ 57,870 RPS
Peak hour RPS = (5B / 86400) × (100 / 10) ≈ 578,700 RPS
Peak minute RPS = 578,700 / 60 ≈ 9,645 RPS

Read operations = 57,870 × 0.7 ≈ 40,509 RPS (average)
Write operations = 57,870 × 0.3 ≈ 17,361 RPS (average)
```

### Storage Requirements
**Assumptions:**
- Data per user: 1 KB (profile, settings)
- Data per transaction: 500 bytes
- Data retention: 3 years

**Calculations:**
```
User profile storage = 100M × 1 KB = 100 GB
Transaction data = 5B requests/day × 500 bytes × 365 × 3 = 2.74 PB
Total storage ≈ 2.75 PB
Replication factor: 3× → 8.25 PB raw storage

Backup storage (weekly snapshots): 8.25 PB × 52 weeks = 429 PB
```

### Network Bandwidth
**Assumptions:**
- Average request size: 2 KB
- Average response size: 5 KB
- Replication overhead: 2× (write to replicas)

**Calculations:**
```
Inbound bandwidth = 57,870 RPS × 2 KB = 115.74 MB/s
Outbound bandwidth = 57,870 RPS × 5 KB = 289.35 MB/s
Replication bandwidth = 17,361 RPS × 2 KB × 2 = 69.44 MB/s
If a dashboard queries 10,000 series over a one-hour range, the system may scan 2.4 million samples at 15-second resolution before rollups; use downsampling and query limits with an explicit fidelity boundary.
```

### Compute Requirements
**Assumptions:**
- Processing time per request: 10 ms
- CPU efficiency: 1 core handles 50 RPS

**Calculations:**
```
CPUs needed for average traffic = 57,870 RPS / 50 = 1,158 cores
CPUs needed for peak traffic = 578,700 RPS / 50 = 11,574 cores
Overprovisioning factor: 1.5× → 17,361 cores total

Using 16 cores per server = 17,361 / 16 ≈ 1,085 servers
With 3:1 replication = 3,255 servers needed
Regional redundancy (3 regions) = 9,765 servers
```

### Latency Analysis (p99)
**Components:**
- Network latency: 5 ms
- Processing: 10 ms
- Storage access: 50 ms (disk), 1 ms (cache)
- Replication write: 20 ms

**Path Analysis:**
```
Cache hit path: 5 + 1 + 5 = 11 ms
Database read path: 5 + 10 + 50 + 5 = 70 ms
Write path: 5 + 10 + 20 + 5 = 40 ms
```

### Cost Estimation
**Monthly costs (approximate):**
```
Compute: 9,765 servers × $1,000/month = $9.765M
Storage: 8.25 PB × $10/GB/month = $82.5M
Bandwidth: 3.8 Tbps × $0.12/GB = $456M
Personnel: 100 engineers × $200K = $20M
Total: ~$568M/month
Cost per user: $5.68/month
```


## Interview Questions & Answers

### Q1: Design the System from Scratch

**Question:** Design a system that can handle 1 billion requests per day with sub-100ms latency.

**Answer Structure:**
1. **Clarify requirements**: DAU, request types, geographic distribution, consistency needs
2. **Back-of-envelope**: Calculate RPS (11.5K avg, 115K peak), storage, bandwidth
3. **High-level design**: Load balancing → services → cache → storage
4. **Deep dive**:
   - Horizontal scaling with sharding
   - Multi-region active-active with eventual consistency
   - Caching strategy (write-through for critical data)
   - Monitoring: metrics, logging, tracing
5. **Bottlenecks**: Identify and address each
6. **Trade-offs**: Consistency vs. availability, latency vs. cost

### Q2: Scaling Challenges

**Question:** You're growing from 10M to 1B users (100x). What breaks and how do you fix it?

**Answer:**
- **Database bottleneck**: Sharding by user ID, consistent hashing, shard rebalancing
- **Cache hit rate drops**: Larger working set, tiered caching (L1: local, L2: distributed)
- **Replication lag**: Write-through for consistency-critical data, eventual consistency elsewhere
- **Operational complexity**: Infrastructure-as-code, auto-scaling, chaos engineering
- **Cost**: Optimize resource utilization, use reserved instances, spot instances for batch

### Q3: Failure Scenarios

**Question:** Your primary database goes down. What happens? How do you recover?

**Answer:**
- **Detection**: Health check timeout (3-5 seconds)
- **Failover**: Automatic promotion of replica using Raft consensus
- **Impact**: Write requests fail for ~10 seconds, reads use replicas
- **Recovery**: Background sync of failed node, re-add to cluster
- **Lessons**: Circuit breakers prevent cascade, bulkhead limits blast radius

### Q4: Consistency Requirements

**Question:** Do you need strong or eventual consistency? Why?

**Answer:**
- **Strong consistency**: Critical for financial transactions, inventory, user auth
  - Implementation: Quorum writes, read-after-write
  - Cost: Higher latency (p99 100ms+), lower throughput

- **Eventual consistency**: Fine for user feeds, recommendations, analytics
  - Implementation: Async replication, read-repair
  - Benefit: Lower latency (p99 <10ms), higher throughput

- **Hybrid approach**: Consistency per operation type, not global

### Q5: Performance Optimization

**Question:** How would you reduce p99 latency from 100ms to 20ms?

**Answer:**
1. **Profile** (measure first): Identify bottleneck (storage, network, compute)
2. **Caching**: Multi-tier (L1 local, L2 distributed), bloom filters for misses
3. **Batching**: Group operations, reduce RPC overhead
4. **Connection pooling**: Reuse TCP connections, reduce handshake latency
5. **Async I/O**: Non-blocking operations, increase parallelism
6. **Database optimization**: Indexing, query optimization, read replicas
7. **Code optimization**: Reduce allocations, use faster algorithms
8. **Hardware**: SSD for storage, faster network interconnects

### Q6: Operational Concerns

**Question:** How do you deploy a new version with zero downtime?

**Answer:**
1. **Canary deployment**: Roll out to 1% of servers, monitor metrics
2. **Gradual rollout**: 1% → 10% → 50% → 100% as confidence increases
3. **Health checks**: Automated rollback if error rate exceeds threshold
4. **Database migration**: Schema changes with backward compatibility
5. **Feature flags**: Toggle features independently of deployment
6. **Monitoring**: Enhanced alerting during rollout, easy incident response


## Technology Stack Recommendations

| Layer | Technology | Why |
|-------|-----------|-----|
| Load Balancing | Nginx, HAProxy, AWS ALB | Distribute traffic, health checks |
| Service Framework | FastAPI (Python), Spring Boot (Java) | Async, built-in monitoring |
| Caching | Redis, Memcached | Sub-millisecond latency, distributed |
| Primary Storage | PostgreSQL, MySQL | ACID, complex queries, reliability |
| Analytics | Elasticsearch, Data Warehouse | Full-text search, time-series analysis |
| Streaming | Kafka, AWS Kinesis | Event processing, real-time |
| Observability | Prometheus, ELK Stack, Jaeger | Metrics, logs, traces |

## Lessons Learned

1. **Premature optimization kills projects**: Start simple, measure, then optimize
2. **Consistency is hard**: Eventually consistent systems are tricky to reason about
3. **Monitoring is non-negotiable**: You can't fix what you can't see
4. **Failure is not rare**: Plan for it, test it, automate recovery
5. **Cost grows with complexity**: Each component adds operational overhead

## Related Topics

- Database design and optimization
- Distributed consensus algorithms
- Load balancing strategies
- Caching mechanisms and patterns
- Monitoring and alerting systems
- Security and compliance


## Back-of-the-Envelope Calculations

**Index Impact:**
- Table: 100M rows, 100 bytes each = 10GB
- Full table scan: 10GB / 500MB/s = 20 seconds
- B-tree index lookup: log₂(100M) ≈ 27 comparisons → <1ms
- Index storage: 100M × 8 bytes (rowid) × 2 (overhead) = 1.6GB

**Query Throughput:**
- Single DB: 10K simple queries/sec
- With connection pool (20 connections): ~5K TPS
- Read replica: 3 replicas → 15K read TPS
- Write throughput limited by leader: 2K TPS
