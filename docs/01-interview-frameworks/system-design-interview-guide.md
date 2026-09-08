# System Design Interview: 4-Phase Framework

**Level:** L3-L5
**Status:** draft
**Audience:** Candidate preparing for a 45–60 minute architecture interview at L4–L5 scope.
**Prerequisites:** HTTP/API basics, storage, caching, queues, replication, and capacity arithmetic.
**Sequence:** Batch 4A, 4/4
**Terra gate:** open
**Time to read:** ~20 min

A proven framework for designing systems during 45-60 minute technical interviews.

## Learning objectives

- Scope requirements and define measurable scale, consistency, availability, and latency targets.
- Produce a request/data-flow diagram and justify storage, cache, queue, and replication choices.
- Deep-dive a bottleneck with capacity math, failure recovery, observability, and rollout behavior.
- Communicate trade-offs and adapt the design when the interviewer changes scale or guarantees.

## Expected outputs

Complete a timed design packet with requirements, out-of-scope decisions, unit-
checked estimates, architecture diagram, API/data model, deep dive, failure
timeline, trade-off table, and closing risks. Review it against a fresh prompt;
re-reading a framework is preparation, not demonstrated design ability.

## Review checkpoints

- **10 minutes:** scope and assumptions are explicit.
- **25 minutes:** major read/write flows and ownership boundaries are drawable.
- **45 minutes:** one hard component includes alternatives, failure recovery, and metrics.
- **Final 5 minutes:** summarize guarantees, bottlenecks, and next investigative steps.

## Phase 1: Requirements & Clarification (5-10 minutes)

**Goal:** Scope the system and agree on constraints before designing.

### Questions to Ask

**Scale:**
- "How many daily active users (DAU)?"
- "What's the expected peak QPS (queries per second)?"

**Features (Prioritize):**
- "What are the core features? Can you rank by importance?"
- "Is this read-heavy or write-heavy?"

**Constraints:**
- "What's the latency requirement? (e.g., P99 < 100ms)"
- "Availability target? (e.g., 99.9% uptime)"
- "Geo-distributed?"

### Template to Fill Out

```
System: [Name]

Scale:
- DAU: _____ million
- Peak QPS: _____

Core Features (ranked):
1. _____
2. _____

Read:Write Ratio: _____:1

Latency SLA: P99 < ___ ms
Availability: ___._%
Data retention: ___ days
```

---

## Phase 2: High-Level Architecture (10-15 minutes)

**Goal:** Sketch the major components and data flow.

### Standard Components

**Entry Point:** Load balancer, API gateway

**Compute:** Stateless API servers, Worker servers

**Data Storage:** Database, Cache layer, Message queue

**Specialized:** Search index, CDN, External services

### Sketch Your Architecture

```
[Users] → [Load Balancer] → [API Servers] 
                               ↓
                           [Cache] → [Database]

[Message Queue] → [Workers]
```

### Key Decisions

1. **Monolith vs. Microservices?** Start with monolith unless clear service boundaries
2. **Sync or Async?** Reads sync, writes can be async
3. **Consistency Model?** Strong (financial) vs. Eventual (social)
4. **Stateless servers?** Yes—push state to external layers

**Validate:** "Does this high-level structure make sense?"

---

## Phase 3: Deep Dive (15-20 minutes)

**Goal:** Design 2-3 critical components in detail. Pick based on system type.

### How to Choose What to Deep Dive

**Read-heavy:** Caching strategy, indexing

**Write-heavy:** Partitioning/sharding, replication

**Low-latency:** CDN placement, caching TTL

**High-availability:** Failover, redundancy

### Example Deep Dive: Caching Strategy

**Decision 1: Technology**
- Redis (fast, data structures)
- Memcached (simple, fast)

**Decision 2: Invalidation Strategy**
- TTL (time-to-live): data expires after time T
- Write-through: cache + DB together
- Write-behind: cache first, async DB

**Decision 3: Cache Hit Ratio Target**
- Aim for 80%+ for read-heavy systems

### Example Deep Dive: Database Design

**Decision 1: SQL vs. NoSQL**
- SQL: ACID, complex queries, structured
- NoSQL: Flexibility, horizontal scaling

**Decision 2: Replication**
- Master-slave: one primary, replicas for reads
- Master-master: multiple primaries, complexity

**Decision 3: Partitioning/Sharding**
- By user_id (vertical), geographic (horizontal), range-based

---

## Phase 4: Trade-offs & Scaling (10-15 minutes)

**Goal:** Discuss alternatives and handle scale increases.

### CAP Theorem

**Consistency (CP):** All reads see latest write (financial systems)

**Availability (AP):** System always responsive, may serve stale data (social feeds)

### Scaling Scenarios

**"What if users 10x?"**
- Load balancer already distributes
- Database: shard by user_id
- Cache: distributed cache cluster
- Workers: auto-scale on queue depth

**"What if one database server goes down?"**
- Replication: promote slave to master
- Detection: heartbeat monitoring
- Failover time: target <10 seconds

**"Latency still too high at P99?"**
- Add CDN for static content
- Add regional caches
- Reduce database round-trips
- Use connection pooling

### Design Trade-offs

**Monolith vs. Microservices:**
- Monolith: simple, fast to build, harder to scale at massive scale
- Microservices: flexible, operational overhead

**SQL vs. Document:**
- Relational: structured, joins, ACID
- Document: flexible, scales easier

**Sync vs. Async:**
- Sync: user waits, simpler
- Async: user gets response immediately, complexity in consistency

---

## Comprehensive Checklist

Use this to ensure you cover all bases:

### Architecture & Components
- [ ] Load balancing strategy
- [ ] API gateway with rate limiting and auth
- [ ] Stateless application servers
- [ ] Database choice (SQL vs. NoSQL)
- [ ] Caching layer and invalidation strategy
- [ ] Message queue for async work
- [ ] Search index if needed (Elasticsearch)
- [ ] CDN for static content

### Data & Storage
- [ ] Schema design (normalization vs. denormalization)
- [ ] Primary key strategy
- [ ] Partitioning/sharding strategy
- [ ] Replication strategy (master-slave, master-master)
- [ ] Backup and recovery strategy
- [ ] Data retention policy

### API & Protocol
- [ ] REST, gRPC, or other?
- [ ] Authentication & authorization
- [ ] Rate limiting & throttling
- [ ] API versioning strategy

### Reliability & Observability
- [ ] Failure modes identified
- [ ] Failover mechanisms
- [ ] Monitoring & alerting (key metrics)
- [ ] Logging strategy (centralized)
- [ ] Distributed tracing
- [ ] Health checks

### Performance
- [ ] Latency targets (P50, P99)
- [ ] Throughput targets (QPS)
- [ ] Connection pooling
- [ ] Batch processing opportunities
- [ ] Query optimization (indexes)

### Security
- [ ] Data encryption (in transit, at rest)
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Rate limiting (DoS)
- [ ] Audit logging

---

## Interview Timeline Example

**45-minute interview:**
- 0-5 min: Clarify requirements
- 5-20 min: High-level architecture
- 20-40 min: Deep dives
- 40-45 min: Trade-offs and scaling

**60-minute interview:**
- 0-10 min: Clarify requirements
- 10-25 min: High-level architecture
- 25-50 min: Deep dives
- 50-60 min: Trade-offs, scaling, follow-ups

---

## Pro Tips

1. **Talk out loud.** Explain your thinking as you design.
2. **Ask clarifying questions early.** Misunderstanding wastes time.
3. **Trade off consciously.** Name the trade-off: "We could use X for Y benefit, but Z trade-off. I choose X because..."
4. **Draw diagrams.** Visual understanding helps.
5. **Validate with interviewer.** After each phase, ask "Does this direction look good?"
6. **Focus on likely bottlenecks.** Pick the component most likely to fail at scale.
7. **Estimate numbers.** QPS, storage, bandwidth—show quantitative thinking.
8. **Mention operational concerns.** Deployments, monitoring, on-call rotations.
9. **Handle follow-ups gracefully.** "Great question! Let me think through that..."
10. **End strong.** Summarize your design in 2-3 sentences, mention trade-offs.
