## System Overview

**Scale Metrics:**
- **Scale:** Ensuring consistency with subset agreement
- **Key Components:** Read quorum, Write quorum, Quorum intersection
- **Primary Use Case:** Distributed databases, consensus, consistency

## Problem Statement

### Functional Requirements
- Read from quorum of replicas for consistency
- Write to quorum of replicas for durability
- Support variable quorum sizes (W + R > N)
- Handle read repair to update stale replicas
- Consistent read-after-write within session

### Non-Functional Requirements
- Consistency: Strong consistency with quorum reads/writes
- Availability: Tolerate up to N - ceil(N/2) failures
- Latency: p99 latency = max(quorum response times)
- Throughput: Quorum parallelism vs serialization
- Network: Reduce replica count to save bandwidth

## Architecture

### High-Level Design

```mermaid
graph TB
    Client["Client Requests"]
    Coordinator["Coordinator/Leader"]
    Nodes["Distributed Nodes<br/>Replicas, Followers"]
    Storage["Persistent Storage<br/>State, Logs"]
    Network["Network Communication<br/>Messages, Replication"]
    Monitor["Monitoring<br/>Health, Metrics"]

    Client -->|Request| Coordinator
    Coordinator -->|Command| Nodes
    Coordinator -->|Log| Storage
    Nodes -->|Sync State| Nodes
    Nodes -->|Persist| Storage
    Network -->|Messages| Coordinator
    Nodes -->|Metrics| Monitor
    Coordinator -->|Metrics| Monitor

    style Coordinator fill:#ff9999
    style Nodes fill:#99ccff
    style Storage fill:#99ff99
    style Network fill:#ffcc99
    style Monitor fill:#cc99ff
```

### Core Concepts

#### Node Roles
- **Coordinator/Leader:** Authoritative decision maker
- **Followers/Replicas:** State replication
- **Learners:** Receiving updates without voting

#### Communication Patterns
- **Synchronous:** Wait for acknowledgments
- **Asynchronous:** Proceed without waiting
- **Quorum:** Majority agreement

#### Failure Models
- **Fail-stop:** Node simply crashes
- **Byzantine:** Node acts maliciously
- **Partition:** Network splits isolate nodes

## Data Flow Scenarios

### Scenario 1: Normal Operation
1. Client sends request to coordinator
2. Coordinator receives request
3. Coordinator logs request durably
4. Coordinator broadcasts to replicas
5. Replicas acknowledge receipt
6. Coordinator responds to client
7. Replicas apply to state machine

### Scenario 2: Node Failure
1. Node stops sending heartbeats
2. Detection timeout expires
3. Leader triggers election or failover
4. New leader elected by quorum
5. New leader catches up on logs
6. System resumes normal operation

### Scenario 3: Network Partition
1. Network splits into partitions
2. One partition has majority (leader)
3. Minority partition cannot operate
4. Majority continues with degraded set
5. Partition heals
6. Minority catches up on missed updates

## Scalability Considerations

### Horizontal Scaling
- Adding more nodes increases availability
- Increases communication overhead
- Quorum size grows
- Decision latency increases

### Consistency vs Scalability
- **Strong consistency:** Requires coordination (slower)
- **Eventual consistency:** Allows divergence (faster)
- Trade-offs based on use case

### Network Topology
- **Star:** Central coordinator (single point of failure)
- **Mesh:** Full connectivity (high overhead)
- **Ring:** Limited connections (failure propagation)

## High Availability & Reliability

### Fault Tolerance
- **Single node failure:** System continues with n-1 nodes
- **Multiple node failures:** Quorum ensures consistency
- **Network partition:** Majority partition continues
- **Byzantine failures:** Classical unauthenticated BFT generally requires 3f+1 replicas for f faulty nodes; Paxos/Raft do not tolerate Byzantine behavior.

### Recovery Mechanisms
- **Log replay:** Reconstruct state from logs
- **Snapshots:** Checkpoint state periodically
- **Catch-up:** Lagging nodes apply missed operations
- **Rebuilding:** Full replication from leader

### Failure Detection
- **Heartbeat:** Periodic signals from leaders
- **Timeout:** Detect failure when signals stop
- **Confirmation:** Multiple failure confirmations before action
- **Distributed:** Gossip-based failure detection

## Data Consistency

### Consistency Models

**Strong Consistency:**
- All reads see latest write
- Requires synchronous replication
- Higher latency, lower availability

**Eventual Consistency:**
- Reads may see stale data
- Asynchronous replication
- Lower latency, higher availability

**Causal Consistency:**
- Causally related operations ordered
- Uncommitted operations visible only to originator
- Balance between strong and eventual

### Ordering Guarantees
- **Total order:** Single serial order for all operations
- **Partial order:** Operations without dependencies are unordered
- **Causal order:** Preserve dependency ordering

## Performance Optimization

### Latency Reduction
- **Batching:** Combine multiple operations
- **Pipelining:** Multiple in-flight requests
- **Caching:** Store frequently accessed data
- **Async:** Non-blocking operations

### Throughput Optimization
- **Replication factor:** Balance durability vs overhead
- **Batching size:** Larger batches = higher overhead but better amortization
- **Parallelism:** Process independent operations concurrently
- **Connection pooling:** Reuse connections

### Resource Efficiency
- **Message compression:** Reduce network bandwidth
- **Incremental updates:** Send only changes
- **Tiered storage:** Hot/cold data management
- **Garbage collection:** Remove old logs/snapshots

## Security Considerations

### Authentication
- Verify node identity
- Prevent unauthorized participation
- Mutual TLS for inter-node communication

### Encryption
- Encrypt data in transit
- Encrypt sensitive data at rest
- Key management and rotation

### Byzantine Resilience
- Verify all messages
- Use cryptographic signatures
- Tolerate f faulty nodes with 3f+1 replicas

## Monitoring & Observability

### Key Metrics
- **Latency:** Request processing time
- **Throughput:** Operations per second
- **Availability:** Uptime percentage
- **Consistency:** Staleness of replicas
- **Replication lag:** How far behind followers are

### Failure Scenarios to Monitor
- Node failures
- Network partitions
- Cascading failures
- Leader election events
- Replication lag spikes

## Common Patterns

### Quorum Reads/Writes
- Ensure consistency with subset of replicas
- Read from quorum: n/2 + 1
- Write to quorum: n/2 + 1

### Linearizability
- All operations appear in a total order
- Reads return most recent write
- Achieved through leader election

### Atomic Broadcast
- All nodes deliver messages in same order
- Tolerance for failures
- Used in consensus protocols

## Technology Stack Comparison

| Aspect | Raft | Paxos | Gossip | CRDT |
|--------|------|-------|--------|------|
| **Consistency** | Strong | Strong | Eventual | CvRDT |
| **Latency** | Low | Medium | High | Very Low |
| **Complexity** | Medium | High | Low | Low |
| **Partition Tolerance** | Yes | Yes | Yes | Yes |
| **Byzantine Safety** | No | No | No | No |

## Lessons Learned

1. **Consensus is Hard:** Multiple rounds of communication needed for safety
2. **Partition Tolerance:** Network failures are inevitable, plan for them
3. **Failure Detection:** Timeouts are imprecise, expect false positives
4. **Replication Lag:** Always present, impacts consistency guarantees
5. **Byzantine Failures:** Rare but catastrophic, require stronger protocols

## Common Interview Questions

1. **Design a distributed lock service**
   - Leader election mechanism
   - Failure handling and timeouts
   - Deadlock prevention

2. **How would you handle network partitions?**
   - Quorum-based decisions
   - Majority partition continues
   - Minority partition waits

3. **What's the difference between Raft and Paxos?**
   - Complexity vs safety tradeoffs
   - When to use each
   - Real-world implementations

4. **How do you detect failures?**
   - Heartbeat mechanisms
   - Timeout tuning
   - False positive handling

5. **Explain eventual consistency**
   - What it guarantees and doesn't
   - When to use it
   - Convergence properties

6. **Design a system that tolerates f Byzantine failures**
   - Need 3f+1 nodes
   - Message authentication
   - Safety and liveness proofs

## Related Systems

- **Consensus:** Raft, Paxos, Zookeeper, Etcd
- **Replication:** Master-slave, Multi-master
- **Failure Detection:** Gossip protocols, Heartbeats
- **Consistency:** Strong, Eventual, Causal
- **Coordination:** Leader election, Distributed locks

---

**Difficulty:** Advanced
**Time to Master:** 3-4 weeks
**Prerequisite Knowledge:** Distributed systems fundamentals, networking
**Common in Interviews:** Yes - Hard problems requiring deep understanding


## Code Implementation

### Python
```python
import asyncio
import aiohttp
from dataclasses import dataclass
from typing import Optional, List
import time, logging

logger = logging.getLogger(__name__)

@dataclass
class ServiceConfig:
    host: str = "localhost"
    port: int = 8080
    timeout_seconds: float = 5.0
    max_retries: int = 3

class ServiceClient:
    """Generic service client with retry and circuit breaker."""
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.base_url = f"http://{config.host}:{config.port}"
        self._failures = 0
        self._circuit_open = False
        self._last_failure: Optional[float] = None

    def _is_circuit_open(self) -> bool:
        if not self._circuit_open:
            return False
        # Half-open after 60s — allow one request through
        if time.time() - self._last_failure > 60:
            self._circuit_open = False
            return False
        return True

    async def call(self, endpoint: str, payload: dict) -> Optional[dict]:
        if self._is_circuit_open():
            logger.warning("Circuit open — fast fail")
            return None

        timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(self.config.max_retries):
                try:
                    async with session.post(
                        f"{self.base_url}{endpoint}", json=payload
                    ) as resp:
                        resp.raise_for_status()
                        self._failures = 0              # reset on success
                        return await resp.json()
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1} failed: {e}")
                    if attempt < self.config.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)  # exponential backoff
            # All retries exhausted
            self._failures += 1
            if self._failures >= 5:                     # open circuit
                self._circuit_open = True
                self._last_failure = time.time()
            return None
```

### Java
```java
import java.net.http.*;
import java.net.URI;
import java.time.Duration;
import java.util.concurrent.atomic.*;
import java.util.concurrent.CompletableFuture;

/** Generic resilient service client with circuit breaker + retry. */
public class ServiceClient {
    private final String baseUrl;
    private final HttpClient http;
    private final AtomicInteger failures = new AtomicInteger(0);
    private final AtomicBoolean circuitOpen = new AtomicBoolean(false);
    private volatile long lastFailureTime;

    public ServiceClient(String host, int port) {
        this.baseUrl = "http://" + host + ":" + port;
        this.http = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();
    }

    private boolean isCircuitOpen() {
        if (!circuitOpen.get()) return false;
        // Half-open after 60s
        if (System.currentTimeMillis() - lastFailureTime > 60_000) {
            circuitOpen.set(false);
            return false;
        }
        return true;
    }

    public CompletableFuture<String> call(String path, String jsonBody) {
        if (isCircuitOpen())
            return CompletableFuture.failedFuture(
                new RuntimeException("Circuit open"));

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + path))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
            .timeout(Duration.ofSeconds(5))
            .build();

        return http.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(resp -> {
                if (resp.statusCode() >= 500) throw new RuntimeException("Server error");
                failures.set(0);  // reset on success
                return resp.body();
            })
            .exceptionally(ex -> {
                if (failures.incrementAndGet() >= 5) {
                    circuitOpen.set(true);
                    lastFailureTime = System.currentTimeMillis();
                }
                return null;
            });
    }
}
```

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
## Follow-up Questions

1. **How would you handle this at 10x the scale described?**
   - What breaks first? (typically: single DB, single cache node, single region)
   - What architectural changes are required?

2. **What are the consistency vs. availability trade-offs in your design?**
   - Where did you accept eventual consistency?
   - Which operations require strong consistency and why?

3. **How would you debug a sudden latency spike in production?**
   - What metrics would you look at first?
   - What's your runbook for the top 3 likely causes?

4. **How does your design handle partial failures?**
   - What happens if one component is slow (not down)?
   - How do you prevent cascading failures?

5. **What would you change if you had to build this in one week vs. six months?**
   - What corners can safely be cut initially?
   - What must be right from day one?

6. **How would you migrate from the current design to a better one without downtime?**
   - What's the strangler-fig or blue-green strategy here?
   - How do you validate correctness during migration?