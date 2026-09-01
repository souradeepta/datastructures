---
title: "System Design Interview Playbook"
interview_type: "System Design / Architecture"
duration: "45-60 minutes"
difficulty: "Advanced"
focus: "Scalability, Trade-offs, Design Patterns"
---

# System Design Interview Playbook

**Level:** L3-L5
**Time to read:** ~10 min

**Duration:** 45-60 minutes  
**Expected Problem:** 1 open-ended system design (e.g., "Design Instagram")  
**Goal:** Propose reasonable architecture, justify design choices, discuss trade-offs

---

## Interview Format

### Time Breakdown (60 min total)
- **0-2 min:** Greeting
- **2-5 min:** Problem statement
- **5-10 min:** Clarify requirements & constraints
- **10-35 min:** High-level architecture & design
- **35-50 min:** Deep dive on 1-2 components
- **50-60 min:** Discuss trade-offs, scalability, follow-ups

---

## What to Expect

**Problem Type:** Open-ended "Design X" system (not a coding problem).

**Examples:**
- Design a URL shortener
- Design a caching system
- Design a messaging queue
- Design a notification system
- Design a search engine

**Evaluation:**
- Do you understand requirements?
- Can you think about scalability?
- Do you know relevant technologies?
- Can you make trade-off decisions?
- Can you dive deep when asked?

---

## System Design Framework (4 Phases)

Use this for ANY system design problem:

### Phase 1: Clarify (5 min)

Ask about:
- **Scale:** How many users? Requests per second? Data storage?
- **Features:** What's required? What's nice-to-have?
- **Constraints:** Latency requirements? Consistency needs?
- **Non-functional:** Availability? Durability? Cost?

Example questions:
- "How many daily active users?"
- "Read-to-write ratio?"
- "Can we tolerate eventual consistency?"
- "What's our latency SLA?"

### Phase 2: High-Level Architecture (15 min)

Design:
- **Client layer** (web, mobile, API)
- **API layer** (REST, gRPC, message queues)
- **Service layer** (business logic)
- **Data layer** (databases, caches)
- **Additional services** (logging, monitoring, auth)

Draw simple boxes and arrows. No details yet.

### Phase 3: Deep Dive (15 min)

Pick 1-2 components and go deep:
- **Database choice:** SQL vs NoSQL? Why?
- **Caching strategy:** What to cache? Invalidation?
- **Scalability:** Horizontal scaling? Load balancing?
- **Consistency:** Strong? Eventual? Transactions?

### Phase 4: Trade-offs & Discussions (10 min)

- What trade-offs did you make?
- What would change if scale increased 10x?
- How would you monitor this system?
- What's the failure mode?

---

## Key Concepts You Must Know

### Foundational
- Vertical vs horizontal scaling
- Load balancing (round-robin, least connections)
- Caching (cache-aside, write-through, write-behind)
- Databases (SQL vs NoSQL, ACID vs BASE)
- Replication (master-slave, master-master)
- Sharding (consistent hashing, range-based)

### Advanced
- Message queues (pub-sub, RabbitMQ, Kafka)
- Consensus (Paxos, Raft, eventual consistency)
- CAP theorem (consistency, availability, partition tolerance)
- Rate limiting (token bucket, sliding window)
- CDNs (content delivery, edge caching)

---

## Sample Problem: Design a URL Shortener

### Clarification
"Let me ask a few questions:
- Approximately how many URL creations per day?
- How long should a shortened URL be?
- Should URLs expire?
- Read-to-write ratio?"

(Assume: 100M URLs/month, 64-bit unique, no expiry, 100:1 read-to-write)

### High-Level Architecture
```
[Client]
    |
[API Gateway/Load Balancer]
    |
[Shortener Service] [Analytics Service]
    |
[Redis Cache] [Database] [Message Queue]
    |
[Analytics DB]
```

### Components
1. **Shortener Service:** Takes long URL, generates short code, stores mapping
2. **Cache:** Store hot mappings (recently created, frequently accessed)
3. **Database:** Persistent store for all URL mappings
4. **Analytics:** Track clicks, geographic data, referrers

### Deep Dive: Database
"For URLs, I'd choose SQL because:
- Fixed schema (source, shortCode, timestamp)
- Need strong consistency (unique codes)
- Can use simple indexing

Sharding strategy:
- Shard by shortCode (consistent hash)
- Allows horizontal scaling
- Easy to lookup"

### Trade-offs
- **Space vs code length:** Longer codes = more URLs
- **Consistency vs availability:** Do we need global uniqueness immediately?
- **Cache vs database:** How much memory vs disk?

---

## Interview Tips

### ✅ Do's
- **Ask lots of questions** — Show thoughtfulness
- **Draw diagrams** — Visual > verbal
- **Explain trade-offs** — Show you think about consequences
- **Know your technologies** — Be ready to justify choices
- **Admit unknowns** — "I'm not sure, but I'd research..."

### ❌ Don'ts
- **Jump to implementation** — This is architecture, not coding
- **Design for scale you don't need** — YAGNI principle
- **Propose bleeding-edge tech** — Proven tech preferred
- **Avoid trade-off discussions** — Interviewers expect nuance
- **Design alone** — Collaborate with interviewer

---

## Follow-Up Questions to Expect

- "How would you handle 10x more traffic?"
- "How would you ensure durability?"
- "What if a database fails?"
- "How would you monitor this?"
- "How would you rollout a change?"
- "What's your backup strategy?"

**Practice:** Be ready for these before the interview.

---

## Optional Practical-Labs Module

Before or after a mock round, use the labs to turn one design discussion into a
small executable model. Choose the lab closest to the interview prompt and
state what the model omits.

- [Distributed-systems labs](../../docs/03-system-design/04-distributed-systems/README.md)
  — reason about quorum intersection, partitioning, and bounded key movement.
- [Event-time streaming lab](../../docs/03-system-design/18-messaging-streaming/README.md)
  — reason about watermarks, lateness, deduplication, and window boundaries.
- [ML/AI systems labs](../../docs/04-ai-ml-llms/EDUCATIONAL_EXAMPLES.md)
  — reason about feature leakage, RAG provenance, and guarded model rollouts.

Outcomes: name the invariant under test, identify one failure or boundary case,
and separate the educational model from the infrastructure a production system
would still need.

Focused commands:

```bash
pytest tests/distributed_systems -q
pytest tests/ml_systems -q
```

## Resources

- [System Design Fundamentals](../domains/system-design-fundamentals.md)
- [Full System Design Guide](../../docs/03-system-design/README.md)
- [Design Patterns](../domains/design-patterns.md)
