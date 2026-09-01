## System Overview

**Scale Metrics:**
- **Scale:** Space-efficient set membership for billions of items
- **Key Components:** Hash functions, Bit arrays, False positives
- **Primary Use Case:** Deduplication, cache optimization, distributed lookups

## Problem Statement

### Functional Requirements
- Check set membership with small false positive rate
- Add elements to the filter structure
- Support multiple hash functions for distributed data
- Count approximate set cardinality (HyperLogLog)
- Merge filters from different partitions

### Non-Functional Requirements
- Space: O(n) bits for n elements
- Time: O(k) hash computations per lookup
- False positives: Configurable p < 1%
- Accuracy: Deterministic membership guarantee
- Distribution: Partition filters across nodes

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
import mmh3, math
from bitarray import bitarray

class BloomFilter:
    """Space-efficient probabilistic set membership."""
    def __init__(self, n: int, fp_rate: float = 0.01):
        self.m = int(-n * math.log(fp_rate) / (math.log(2) ** 2))
        self.k = int(self.m / n * math.log(2))
        self.bits = bitarray(self.m)
        self.bits.setall(0)

    def add(self, item: str) -> None:
        for seed in range(self.k):
            idx = mmh3.hash(item, seed) % self.m
            self.bits[idx] = 1

    def contains(self, item: str) -> bool:
        """Returns True if item MIGHT be in set; False = definitely not."""
        return all(self.bits[mmh3.hash(item, s) % self.m] for s in range(self.k))

bf = BloomFilter(n=1_000_000, fp_rate=0.01)
bf.add("user:abc123")
print(bf.contains("user:abc123"))   # True (in set)
print(bf.contains("user:xyz999"))   # False (not in set)
```

### Java
```java
import java.util.BitSet;

public class BloomFilter {
    private final BitSet bits;
    private final int m, k;

    public BloomFilter(int n, double fpRate) {
        this.m = (int) (-n * Math.log(fpRate) / (Math.log(2) * Math.log(2)));
        this.k = (int) (m / n * Math.log(2));
        this.bits = new BitSet(m);
    }

    private int hash(String item, int seed) {
        // MurmurHash simulation using Java hashCode
        int h = item.hashCode() ^ (seed * 0x9e3779b9);
        return Math.abs(h) % m;
    }

    public void add(String item) {
        for (int i = 0; i < k; i++) bits.set(hash(item, i));
    }

    public boolean mightContain(String item) {
        for (int i = 0; i < k; i++) if (!bits.get(hash(item, i))) return false;
        return true;
    }

    public static void main(String[] args) {
        BloomFilter bf = new BloomFilter(1_000_000, 0.01);
        bf.add("user:abc123");
        System.out.println(bf.mightContain("user:abc123")); // true
        System.out.println(bf.mightContain("user:xyz999")); // false
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