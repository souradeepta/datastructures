# Parking Lot System

Status: draft

Audience: Backend engineers preparing for object modeling, allocation, and concurrency interviews.

Prerequisites: Object-oriented design, indexing, reservations, and transactional state changes.

Sequence: Model spot eligibility → allocate atomically → reconcile occupancy and payment state.

Terra gate: Before coding, state how two entry gates avoid assigning the same spot and how a stale availability display is corrected.

## Problem Statement

Design a parking lot system with multiple levels, different spot sizes, and availability tracking.

**Requirements:**
- Multiple levels/floors
- Different vehicle types (compact, regular, large)
- Find available spot
- Parking/unparking
- Availability display


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

## Design

### Object Model

```
ParkingLot
  ├── Level[]
      ├── Spot[] (each marked by size, occupied status)
      └── availableSpots tracking

Vehicle types: COMPACT, REGULAR, LARGE (in increasing size)
Spot sizes: match vehicle types
```

### Key Classes

```
Vehicle: type, license_plate
Spot: number, level, size, occupied, parked_vehicle
Level: floor_number, spots[], available_counts
ParkingLot: levels, display()
```

### Find Available Spot Algorithm

```
for each level:
  for each spot in level:
    if spot.size >= vehicle.size and not occupied:
      return spot
return None  // No spot available
```

### State Tracking

```
For each spot size, track available count:
  available_compact = 3
  available_regular = 7
  available_large = 2

Update on park/unpark operations
```


## Scenario

Parking Lot System is a critical component in modern distributed systems. In real-world applications, managing finite resources with efficient allocation and lookup. For example, major tech companies like Netflix, Uber, and Airbnb rely on similar solutions to handle millions of concurrent users and requests. The challenge is achieving this while maintaining sub-100ms latency, 99.99% availability, and gracefully handling 10x traffic spikes during peak demand. This component provides the foundational capability to solve these challenges reliably and efficiently at global scale.

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

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│      ParkingLot                             │
│  ┌──────────────────────────────────────┐   │
│  │  Level 3 (top)                       │   │
│  │  [C] [C] [R] [R] [R] [L] [L]        │   │
│  │  Available: C=1, R=2, L=2            │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Level 2 (middle)                    │   │
│  │  [C] [X] [X] [R] [R] [X] [L]        │   │
│  │  X=occupied, Available: C=0, R=1, L=0   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Level 1 (ground)                    │   │
│  │  [X] [X] [X] [X] [X] [X] [X]        │   │
│  │  Full, No available spots            │   │
│  └──────────────────────────────────────┘   │
│         ↓ (parking operations)               │
│  ┌──────────────────────────────────────┐   │
│  │  ParkingSpot Manager                 │   │
│  │  - Find available spot by size       │   │
│  │  - Track occupancy (HashMap)         │   │
│  │  - Update level counters             │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Back-of-Envelope Calculations

For typical 5-level parking lot, 50 spots per level (250 total):
- Storage: 250 spots × 50 bytes/spot (location, size, vehicle_ref) = 12.5KB local memory
- Throughput: ~100 arrivals/departures per hour, 2 sec per operation = no bottleneck
- Latency: Find spot O(n) = 250 spot checks ≈ 1ms, Display O(1) ≈ 100μs
- Availability update: O(1) counter increment, < 1μs

Multi-garage system (10 parking lots): aggregate availability in ~1ms via cache.

## Design Choice Comparison

| Approach | Pros | Cons |
|----------|------|------|
| Linear scan per level | Simple, works for <1000 spots | O(n) per find, slow |
| Available count tracking | O(1) availability checks | Must maintain counters |
| Heap/PQ by distance | Finds closest spot quickly | More complex, extra space |

## Follow-up Interview Questions

1. How would you design for a 1000-level mega-structure? Need distributed system with regional coordinators.
2. What if a vehicle doesn't exit—how to detect and handle abandoned cars?
3. How to optimize for peak hour (1000 arrivals/hour)? Add reservation system, predict availability.
4. What's the bottleneck at 10x scale? DB writes for persistence, not the algorithm (still O(1)).
5. How would you implement handicap spot priority and reservations?

## Example Scenario Walkthrough

Initial state: 3-level lot with 3 spots each (C=compact, R=regular, L=large)

Level 1: [C] [R] [L] — all empty
Level 2: [C] [R] [L] — all empty  
Level 3: [C] [R] [L] — all empty
Available: C=3, R=3, L=3

Step 1: Regular vehicle arrives (size REGULAR)
- Check availability: R=3, available ✓
- Scan Level 1: Spot 2 (R) is empty
- Park vehicle: Level1, Spot 2
- Update: Available R=2
- Status: PARKED, Level 1 Spot 2

Step 2: Large vehicle arrives (size LARGE)
- Check availability: L=3, available ✓
- Scan Level 1: Spot 3 (L) is empty
- Park vehicle: Level 1, Spot 3
- Update: Available L=2
- Status: PARKED, Level 1 Spot 3

Step 3: Oversized truck arrives (size XLARGE)
- Check availability: L=2, but no XLARGE size
- Scan all spots: no XLARGE match
- Return: NO SPOT AVAILABLE (oversize vehicle)
- Status: NOT PARKED, try another lot

Step 4: Regular vehicle exits
- Unpark: Level 1, Spot 2
- Available: R=3
- Status: EMPTY, ready for next car


### Python Implementation

```python
from enum import Enum
from typing import Optional

class VehicleSize(Enum):
    COMPACT = 1
    REGULAR = 2
    LARGE = 3

class ParkingSpot:
    def __init__(self, spot_number: int, size: VehicleSize):
        self.spot_number = spot_number
        self.size = size
        self.occupied = False
        self.vehicle = None

    def is_available(self) -> bool:
        return not self.occupied

    def park_vehicle(self, vehicle):
        if self.occupied:
            raise Exception("Spot already occupied")
        self.occupied = True
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.occupied = False
        self.vehicle = None

class Level:
    def __init__(self, level_number: int, num_spots: int):
        self.level_number = level_number
        self.spots = []
        self.available_count = {size: 0 for size in VehicleSize}

        # Create spots (30% compact, 50% regular, 20% large)
        compact = int(num_spots * 0.3)
        regular = int(num_spots * 0.5)
        large = num_spots - compact - regular

        spot_num = 0
        for _ in range(compact):
            self.spots.append(ParkingSpot(spot_num, VehicleSize.COMPACT))
            spot_num += 1

        for _ in range(regular):
            self.spots.append(ParkingSpot(spot_num, VehicleSize.REGULAR))
            spot_num += 1

        for _ in range(large):
            self.spots.append(ParkingSpot(spot_num, VehicleSize.LARGE))
            spot_num += 1

        self._update_available()

    def find_available_spot(self, size: VehicleSize) -> Optional[ParkingSpot]:
        for spot in self.spots:
            if spot.is_available() and spot.size.value >= size.value:
                return spot
        return None

    def park_vehicle(self, vehicle, size: VehicleSize) -> Optional[ParkingSpot]:
        spot = self.find_available_spot(size)
        if spot:
            spot.park_vehicle(vehicle)
            self._update_available()
        return spot

    def unpark_vehicle(self, spot: ParkingSpot):
        spot.remove_vehicle()
        self._update_available()

    def _update_available(self):
        for size in VehicleSize:
            self.available_count[size] = sum(
                1 for spot in self.spots
                if spot.is_available() and spot.size == size
            )

    def get_available_count(self, size: VehicleSize) -> int:
        return self.available_count.get(size, 0)

class ParkingLot:
    def __init__(self, num_levels: int, spots_per_level: int):
        self.levels = [Level(i, spots_per_level) for i in range(num_levels)]

    def park_vehicle(self, vehicle, size: VehicleSize) -> bool:
        for level in self.levels:
            if level.get_available_count(size) > 0:
                spot = level.park_vehicle(vehicle, size)
                if spot:
                    print(f"Vehicle {vehicle} parked at L{level.level_number}:S{spot.spot_number}")
                    return True
        print("No available spot")
        return False

    def unpark_vehicle(self, level_num: int, spot_num: int):
        level = self.levels[level_num]
        spot = level.spots[spot_num]
        level.unpark_vehicle(spot)
        print(f"Vehicle {spot.vehicle} unparked")

    def display_availability(self):
        for level in self.levels:
            print(f"Level {level.level_number}:")
            for size in VehicleSize:
                print(f"  {size.name}: {level.get_available_count(size)}")

# Usage
lot = ParkingLot(3, 10)
lot.park_vehicle("CAR1", VehicleSize.COMPACT)
lot.park_vehicle("CAR2", VehicleSize.REGULAR)
lot.park_vehicle("TRUCK1", VehicleSize.LARGE)
lot.display_availability()
```

### Java Implementation

```java
import java.util.*;

enum VehicleSize {
    COMPACT(1), REGULAR(2), LARGE(3);
    private int value;
    VehicleSize(int value) { this.value = value; }
    public int getValue() { return value; }
}

class ParkingSpot {
    private int spotNumber;
    private VehicleSize size;
    private String vehicle;

    public ParkingSpot(int spotNumber, VehicleSize size) {
        this.spotNumber = spotNumber;
        this.size = size;
        this.vehicle = null;
    }

    public boolean isAvailable() { return vehicle == null; }
    public void parkVehicle(String vehicle) { this.vehicle = vehicle; }
    public void removeVehicle() { this.vehicle = null; }
    public boolean canFit(VehicleSize size) {
        return this.size.getValue() >= size.getValue();
    }
}

class Level {
    private int levelNumber;
    private List<ParkingSpot> spots;

    public Level(int levelNumber, int numSpots) {
        this.levelNumber = levelNumber;
        this.spots = new ArrayList<>();

        int compact = (int)(numSpots * 0.3);
        int regular = (int)(numSpots * 0.5);
        int large = numSpots - compact - regular;

        int spotNum = 0;
        for (int i = 0; i < compact; i++)
            spots.add(new ParkingSpot(spotNum++, VehicleSize.COMPACT));
        for (int i = 0; i < regular; i++)
            spots.add(new ParkingSpot(spotNum++, VehicleSize.REGULAR));
        for (int i = 0; i < large; i++)
            spots.add(new ParkingSpot(spotNum++, VehicleSize.LARGE));
    }

    public ParkingSpot findAvailableSpot(VehicleSize size) {
        for (ParkingSpot spot : spots) {
            if (spot.isAvailable() && spot.canFit(size)) {
                return spot;
            }
        }
        return null;
    }

    public boolean parkVehicle(String vehicle, VehicleSize size) {
        ParkingSpot spot = findAvailableSpot(size);
        if (spot != null) {
            spot.parkVehicle(vehicle);
            return true;
        }
        return false;
    }
}

class ParkingLot {
    private List<Level> levels;

    public ParkingLot(int numLevels, int spotsPerLevel) {
        this.levels = new ArrayList<>();
        for (int i = 0; i < numLevels; i++) {
            levels.add(new Level(i, spotsPerLevel));
        }
    }

    public boolean parkVehicle(String vehicle, VehicleSize size) {
        for (Level level : levels) {
            if (level.parkVehicle(vehicle, size)) {
                return true;
            }
        }
        return false;
    }
}
```

### Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Entrance
    Entrance --> CheckAvailability
    CheckAvailability --> AvailableSpots
    AvailableSpots --> GetTicket
    GetTicket --> Park
    Park --> Parked
    Parked --> CheckOut
    CheckOut --> Payment
    Payment --> Exit
    Exit --> [*]
```

## Implementation Discussion

**Design Choices:**
- Separate spot size classes (avoids enum comparison issues)
- Level abstraction for scalability
- Available count tracking (O(1) lookup)

**Optimization:**
```python
# Use heap for finding closest available spot
import heapq

class OptimizedLevel:
    def __init__(self):
        self.available_heaps = {
            VehicleSize.COMPACT: [],
            VehicleSize.REGULAR: [],
            VehicleSize.LARGE: []
        }

    def find_closest_spot(self, size):
        # O(log n) instead of O(n)
        return heapq.heappop(self.available_heaps[size])
```

**Production Features:**
- Payment tracking (entry/exit times)
- Handicap spot priority
- Reservation system
- Analytics (occupancy rate)


## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| findSpot | O(n) where n=total spots | O(1) |
| parkVehicle | O(1) | O(1) |
| unparkVehicle | O(1) | O(1) |
| getAvailability | O(1) | O(1) |
| Space | — | O(n) |

## Edge Cases

1. No spots available
2. Vehicle type larger than all available spots
3. Unpark from wrong spot
4. Multiple vehicles with same license plate

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
Assume a 5,000-space facility with 6 entry/exit lanes handling 120 arrivals and 100 departures per minute at peak.
Maintain per-vehicle-type free-space indexes so allocation is O(log n) or O(1) depending on the chosen queue/set structure; reserve a spot transactionally before opening the gate.
Availability displays may be eventually consistent, but the authoritative spot state must reject duplicate assignments and reconcile abandoned reservations.
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
At 220 gate events/minute and a 2 KB event record, the durable event stream is under 8 KB/s; operational complexity is dominated by correctness, device retries, and reconciliation rather than bandwidth.
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

**System Load Estimation:**
- 1M daily active users × 10 requests/day = 10M requests/day
- Peak QPS = 10M / 86400 × 3 (peak factor) ≈ 350 QPS
- API server capacity: 1000 QPS/server → 1 server sufficient at peak
- With 2x redundancy: 2 servers minimum

**Storage Estimation:**
- 1M users × 10KB average data = 10GB structured data
- Annual growth: 10GB × 365 = 3.65TB/year
- With 3x replication: 11TB/year
- SSD cost ($0.10/GB): $1,100/year

**Bandwidth:**
- 350 QPS × 10KB response = 3.5MB/sec outbound
- Monthly egress: 3.5MB × 86400 × 30 = 9TB/month
