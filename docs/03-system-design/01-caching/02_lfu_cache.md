# LFU Cache

Status: draft

Audience: Backend engineers preparing for cache implementation and eviction-policy interviews.

Prerequisites: Hash maps, linked lists, amortized O(1) operations, and cache consistency.

Sequence: Define hit/miss semantics → maintain frequency buckets → choose capacity and invalidation policy.

Terra gate: Before coding, state how ties are broken, what happens at capacity zero, and whether updates count as accesses.

## Problem Statement

Implement an LFU (Least Frequently Used) Cache with fixed capacity. When capacity is exceeded, evict the least frequently used item. Break ties using LRU (least recently used among items with same frequency).

**Operations:**
- `get(key)` — return value, increment frequency
- `put(key, value)` — insert/update, evict LFU+LRU if over capacity

**Constraints:**
- Both operations must be O(1)
- Frequency tracked per key
- Ties broken by recency

## Scenario

LFU Cache is a critical component in modern distributed systems. In real-world applications, serving billions of user interactions with minimal latency. For example, major tech companies like Netflix, Uber, and Airbnb rely on similar solutions to handle millions of concurrent users and requests. The challenge is achieving this while maintaining sub-100ms latency, 99.99% availability, and gracefully handling 10x traffic spikes during peak demand. This component provides the foundational capability to solve these challenges reliably and efficiently at global scale.

## Users

- **Backend Engineers**: Responsible for implementing and maintaining this system component in production environments. They need to understand the architecture, trade-offs, failure modes, and operational considerations.
- **DevOps/SRE Teams**: Monitor system health, manage scaling policies, handle incidents, and ensure reliability SLAs are met. They need insights into performance characteristics, bottlenecks, and failure recovery mechanisms.
- **Data Engineers**: Design data pipelines and analytics around this system, requiring deep understanding of data flow, consistency guarantees, and throughput characteristics.
- **System Architects**: Make high-level architectural decisions that impact company infrastructure, requiring comprehensive understanding of capabilities, limitations, and scalability boundaries.
- **Security Teams**: Understand security implications, potential vulnerabilities, and compliance requirements for this component.

## PRD

### Functional Requirements
- Core operations work correctly
- Explicit error handling
- Consistency guarantees defined
- Monitoring and observability

### Non-Functional Requirements
- Performance targets met
- Availability SLA achieved
- Scalability headroom
- Cost efficient

### Success Metrics
- Benchmarks met
- Uptime targets met
- Resource budgets
- No data loss


## Flow

The typical operational flow for this system involves these key phases:

1. **Request Arrival**: Client/upstream system sends request with required parameters and context
2. **Validation & Routing**: System validates request format, authentication, and routes to correct handler/shard/instance
3. **Core Processing**: Execute the main algorithm, database query, or business logic on the data/state
4. **State Management**: Update internal state (caches, indexes, counters, logs) with proper atomicity and locking
5. **Response Generation**: Format results and return to requester with relevant metadata (timing, version info)
6. **Observability**: Record metrics (latency, throughput, errors), logs (for debugging), and traces (for performance analysis)

This flow repeats thousands or millions of times per second in production. Each operation's efficiency compounds across the entire system, making careful optimization essential. Bottlenecks at any phase can cascade to impact overall system performance.


## Code Explanation (Detailed)

### Implementation Approach
The code demonstrates core patterns and trade-offs.

### Key Operations
Each operation shows algorithm and performance characteristics.

### Concurrency and Atomicity
Locking strategies, race condition prevention.

### Edge Cases
Boundary conditions and error handling.

### Performance Optimization
Techniques for reducing latency and throughput.

## Architecture Diagram

```
┌──────────────────────────────────────┐
│     LFU Cache (capacity=3)           │
├──────────────────────────────────────┤
│  freq_map: {key -> frequency}        │
│  {1: 3, 2: 1, 3: 2}                  │
├──────────────────────────────────────┤
│  freq_list: {freq -> keys (ordered)} │
│  {1: [2], 2: [3], 3: [1]}            │
├──────────────────────────────────────┤
│  min_freq: 1 (track minimum)         │
└──────────────────────────────────────┘
```

## Design

### Data Structures

```
freq_map: {key -> freq}        (track frequency per key)
freq_list: {freq -> OrderedDict of keys}  (keys with each frequency, ordered by recency)
min_freq: int                   (current minimum frequency)
```

**Why:**
- `freq_map` gives O(1) frequency lookup
- `freq_list` allows O(1) LFU+LRU eviction
- OrderedDict preserves insertion order (most recent at end)

### Key Operations

```
GET(key):
  - Increment freq[key]
  - Move key from freq_list[old_freq] to freq_list[new_freq]
  - If freq_list[old_freq] empty and old_freq == min_freq: min_freq++
  - Return value

PUT(key, value):
  - If over capacity: evict from freq_list[min_freq][0] (oldest)
  - Insert/update with freq=1, set min_freq=1
```

#
### Python Implementation

```python
from collections import defaultdict
from typing import Optional

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.freq_map = defaultdict(list)      # freq -> [keys]
        self.key_freq = {}                      # key -> freq
        self.key_value = {}                     # key -> value

    def get(self, key: int) -> int:
        if key not in self.key_value:
            return -1

        self._increase_freq(key)
        return self.key_value[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.key_value:
            self.key_value[key] = value
            self._increase_freq(key)
            return

        if len(self.key_value) >= self.capacity:
            self._evict_lfu()

        self.key_value[key] = value
        self.key_freq[key] = 1
        self.freq_map[1].append(key)
        self.min_freq = 1

    def _increase_freq(self, key: int) -> None:
        freq = self.key_freq[key]
        self.key_freq[key] = freq + 1

        # Remove from old freq list
        self.freq_map[freq].remove(key)

        # Add to new freq list
        self.freq_map[freq + 1].append(key)

        # Update min_freq if needed
        if len(self.freq_map[freq]) == 0 and freq == self.min_freq:
            self.min_freq = freq + 1

    def _evict_lfu(self) -> None:
        # Evict LFU (first in list at min_freq)
        lfu_key = self.freq_map[self.min_freq].pop(0)
        del self.key_value[lfu_key]
        del self.key_freq[lfu_key]

# Usage
cache = LFUCache(2)
cache.put(1, 1)   # freq: {1: 1}
cache.put(2, 2)   # freq: {1: [1,2]}
cache.get(1)      # freq: {1: [2], 2: [1]}
cache.put(3, 3)   # evict 2 (freq=1), freq: {2: [1], 1: [3]}
```

### Java Implementation

```java
import java.util.*;

class LFUCache {
    private int capacity;
    private int minFreq;
    private Map<Integer, Integer> keyValue;
    private Map<Integer, Integer> keyFreq;
    private Map<Integer, LinkedList<Integer>> freqList;

    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.minFreq = 0;
        this.keyValue = new HashMap<>();
        this.keyFreq = new HashMap<>();
        this.freqList = new HashMap<>();
    }

    public int get(int key) {
        if (!keyValue.containsKey(key)) return -1;
        increaseFreq(key);
        return keyValue.get(key);
    }

    public void put(int key, int value) {
        if (capacity <= 0) return;

        if (keyValue.containsKey(key)) {
            keyValue.put(key, value);
            increaseFreq(key);
            return;
        }

        if (keyValue.size() >= capacity) {
            evictLFU();
        }

        keyValue.put(key, value);
        keyFreq.put(key, 1);
        freqList.computeIfAbsent(1, k -> new LinkedList<>()).add(key);
        minFreq = 1;
    }

    private void increaseFreq(int key) {
        int freq = keyFreq.get(key);
        keyFreq.put(key, freq + 1);

        freqList.get(freq).remove(Integer.valueOf(key));
        freqList.computeIfAbsent(freq + 1, k -> new LinkedList<>()).add(key);

        if (freqList.get(freq).isEmpty() && freq == minFreq) {
            minFreq = freq + 1;
        }
    }

    private void evictLFU() {
        int lfuKey = freqList.get(minFreq).removeFirst();
        keyValue.remove(lfuKey);
        keyFreq.remove(lfuKey);
    }
}
```

### Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Request
    Request --> CacheCheck
    CacheCheck --> Hit: Found
    CacheCheck --> Miss: Not Found
    Hit --> UpdateFreq
    UpdateFreq --> Return
    Miss --> Fetch
    Fetch --> Cache
    Cache --> UpdateFreq
    Return --> [*]
```

## Implementation Discussion

**Why separate maps?**
- keyValue: store actual data
- keyFreq: track frequency for each key
- freqList: quickly find all keys at a frequency

**Tie-breaking (LRU within same frequency):**
- LinkedList maintains insertion order
- Oldest key at frequency F evicted first
- Achieved via removeFirst() on LRU in freq list

**Complexity Analysis:**
- get/put: O(1) average, all operations on HashMap/LinkedList
- Space: O(capacity + frequencies)

**Optimization for Production:**
```python
class OptimizedLFUCache:
    def __init__(self, capacity: int):
        # Cache hot items (high frequency)
        self.hot_cache = {}  # Direct access, no re-hashing
        # Maintain freq separately for better cache locality
        self.freqs = []      # Index by key for O(1) lookup
```

**Edge Cases:**
- Frequency overflow: cap at max frequency or use sliding window
- Capacity=1: works, always evict and add new item
- Get on missing key: return -1, don't create entry


## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| get | O(1) | — |
| put | O(1) | — |
| Space | — | O(capacity) |

## Back-of-Envelope Calculations

Cache 10K items, frequency distribution (80% access 1 time, 20% access 5+ times):
- Storage: 10K × (8 + 8 + overhead) = 160KB + overhead
- Access distribution: 8K items freq=1, 2K items freq=5+
- On eviction: Remove from 8K pool (LFU)
- Hit rate with distribution: ~70% (2K items get 80% traffic)

## Design Choices

| Approach | Pros | Cons |
|----------|------|------|
| HashMap + FreqList | O(1) all ops | Complex state |
| Heap + HashMap | Simple | O(log n) update |
| Array of queues | Memory efficient | Hash collisions |

## Example Walkthrough

Sequence: put(1,1), put(2,2), get(1), put(3,3), put(4,4), get(1), evict?

```
put(1,1): Cache={1:1}, freq={1:1}, freq_list={1:[1]}, min_freq=1
put(2,2): Cache={1:1,2:2}, freq={1:1,2:1}, freq_list={1:[1,2]}, min_freq=1
get(1): freq={1:0,2:1}, freq_list={1:[2],2:[1]}, min_freq=1
put(3,3): Cache full, evict key with freq=1 (tie=2), freq={1:1,2:1,3:1}
put(4,4): Cache full, evict 1 from freq=1, freq={2:1,3:1,4:1}
get(1): Miss! Evicted. freq_list={1:[3,4,2]}
```

## Trade-offs

| Trade-off | Option A | Option B |
|-----------|----------|----------|
| Accuracy vs Speed | Perfect LFU (O(log n)) | Approximate LFU (O(1)) |
| Memory | Freq histogram | Full freq_list |
| Tie-breaking | LRU (complex) | FIFO (simple) |

## Real-World Use Cases

- Database indices (hot data)
- CDN edge caches (popular content)
- CPU cache (predicted reuse)
- Memory allocation (frequently used pages)
- Recommendation systems (popular items)

## Common Questions & Answers

**Q: What is caching and why do we need it?**

A: Caching stores frequently accessed data in fast storage (memory) to reduce latency and load on slower backends (database). Trade space (cache) for speed (latency). Critical for systems serving millions of requests per second.

**Q: What are the main cache eviction policies?**

A: LRU (least recently used), LFU (least frequently used), FIFO (first in first out), TTL (time-based), Random, and ARC (adaptive replacement). Choose based on access patterns: LRU for temporal, LFU for frequency, TTL for time-sensitive data.

**Q: What is cache hit rate and cache miss rate?**

A: Hit rate = successful_finds / total_accesses. Miss rate = 1 - hit rate. P(hit) = hits / (hits + misses). Target 80%+ hit rates for effective caching. Too-small cache gives low hit rate (wasted resources). Too-large cache uses more memory than needed.

**Q: How do you handle cache invalidation when backend data changes?**

A: Use TTL (time-based expiration), active invalidation (notify cache on write), cache-aside pattern (client checks backend), or write-through (update both). Active invalidation is fastest but complex. TTL is simplest but has stale data window.

**Q: What is the cache-aside pattern?**

A: Application checks cache first. On miss, fetch from backend, update cache, then return. Simple to implement. Risk: race condition where multiple threads fetch same miss simultaneously (thundering herd problem).

**Q: What is write-through caching?**

A: Writes go to both cache and backend simultaneously (synchronously). Ensures consistency: read always gets latest. Cost: write latency includes backend write. Safer than write-back but slower.

**Q: What is write-back (write-behind) caching?**

A: Writes go to cache only; backend updated asynchronously later (batch or periodic). Fast writes. Risk: data loss if cache fails before flushing. Need durability guarantees (persistence, replication).

**Q: How do you choose cache size?**

A: Estimate working set (frequently accessed data volume). Add 20-30% buffer for margin. Monitor hit rate: if < 80%, increase size. If > 95%, might be oversized (waste). Use tools like cachegrind to profile.

**Q: What's the difference between client-side and server-side caching?**

A: Client cache (browser): reduces network round-trips, entirely controlled by client. Server cache (memory, Redis): shared across clients, controlled by server. Multi-level caching often best.

**Q: How do you measure cache effectiveness?**

A: Hit rate (primary metric), latency reduction (P99 latency with vs. without cache), backend load reduction, and memory cost per cache entry. Calculate ROI: cost of cache vs. benefit (reduced latency, backend load).

## Follow-up Questions & Answers

**Q: How do you prevent the thundering herd problem in caches?**

A: When popular key expires, many threads fetch from backend simultaneously causing spike. Solutions: probabilistic early expiration (refresh before TTL), request coalescing (single thread rebuilds, others wait), or bloom filters (detect non-existent keys fast).

**Q: How would you implement multi-level cache hierarchy?**

A: Use L1 (fast, small, in-process), L2 (medium, local machine), L3 (large, remote, Redis). Check L1, miss→L2, miss→L3, miss→backend. On write: update all levels. Trade space for speed across levels.

**Q: Can you implement read-through caching (automatic population)?**

A: Yes, cache loader/resolver called on miss. Transparent to application. Backend automatically uses cache layer. More complex than cache-aside but cleaner separation.

**Q: How do you handle hot keys in distributed caches?**

A: Hot key = key accessed by many threads/clients. Replicate hot keys on multiple cache nodes. Use local in-process caches for very hot keys. Monitor and detect hot keys automatically.

**Q: What's the difference between warm and cold cache startup?**

A: Cold cache: empty at start, misses until populated (slow ramp-up). Warm cache: pre-loaded from previous state (RDB/snapshot). Warm startup is critical for production (instant performance).

**Q: How would you measure cache effectiveness for business metrics?**

A: Track hit rate, P99 latency (with/without cache), backend QPS reduction, revenue impact. Calculate cache size vs. cost savings. A/B test to prove business value.

**Q: What happens when cache size is insufficient for working set?**

A: Constant evictions = high miss rate = ineffective cache. Solution: increase cache size, improve eviction policy, reduce working set, or use better hardware (faster storage).

**Q: How do you debug cache issues in production?**

A: Monitor hit rate continuously. Profile cache keys (which keys are accessed). Check for cache stampedes (sudden miss spike). Use distributed tracing to see cache path.

**Q: How would you implement a persistent cache?**

A: Combine memory cache (fast) with persistent backend (database, RocksDB, LevelDB). Write-back pattern: batch updates to persistent store. Trade latency for durability.

**Q: Can you use caching for write-heavy workloads?**

A: Write caching is risky (consistency issues). Use carefully: write-through for safety, write-back for speed. Good for batch writes (aggregate before writing). Monitor durability guarantees.


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
Assume a 1 million-entry cache serving 200,000 get/put operations/s, with a 95% get rate.
The O(1) design performs one hash lookup plus frequency-bucket unlink/relink per operation; memory is O(capacity) for entries, buckets, and recency links.
Evicting the least-frequent item protects long-lived hot data, but a scan-resistant workload may still need admission control or periodic frequency aging.
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
If an average cached value is 2 KB, a 200,000-operation/s workload represents about 400 MB/s of logical value access; network bandwidth depends on the hit rate and client payloads.
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

**Cache Sizing:**
- Working set: 10M active items × 1KB avg = 10GB
- 80% hit target → cache needs to hold top 20% most popular = 2GB
- With 10 cache nodes: 200MB per node (fits in RAM)
- Hit ratio math: 80% from cache, 20% from DB
- Effective latency: 0.8×1ms + 0.2×10ms = 2.8ms (vs 10ms without cache)

**Throughput:**
- Single Redis node: 100K ops/sec
- 10-node cluster: 1M ops/sec
- At 50% hit ratio a 1M QPS app issues 500K DB queries — unsustainable
- At 90% hit ratio: 100K DB queries — manageable
