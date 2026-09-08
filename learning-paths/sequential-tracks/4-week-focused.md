---
title: "4-Week Focused Interview Prep"
duration: "4 weeks"
commitment: "6-7 hours/week"
difficulty: "Moderate"
best_for: "Balanced preparation for all interview types"
---

# 4-Week Focused Interview Prep

**Level:** L3-L5
**Status:** draft
**Audience:** Candidate with four weeks and 6–7 hours per week preparing for coding and system-design interviews.
**Prerequisites:** Python basics, arrays/strings familiarity, and access to the maintained pytest workflow.
**Sequence:** Batch 4A, 1/4
**Terra gate:** open
**Time to read:** ~10 min

**Total Time:** ~24-28 hours  
**Pace:** 6-7 hours/week  
**Target:** Solid coverage of core data structures and algorithms

## Learning objectives

By the end of this track, you should be able to:

- Clarify constraints, select a tractable algorithm, implement it, and state complexity under interview time pressure.
- Solve representative array, string, tree, graph, heap, and dynamic-programming problems with tested Python code.
- Explain a system-design proposal with requirements, capacity assumptions, failure modes, and trade-offs.
- Diagnose weak areas using weekly evidence rather than treating completed reading as mastery.

## Expected outputs

Produce one checked artifact each week: a small set of solved problems with
tests, a short complexity log, and one spoken explanation or design sketch.
By the end, retain four artifacts: a corrected coding solution, a data-structure
implementation, a system-design diagram with a capacity estimate, and a timed
mock-interview retrospective. Use the repository's maintained Python and pytest
trees where an implementation exists; a checklist alone is not evidence.

## How to use the checkpoints

At each weekly checkpoint, mark a skill complete only after solving a fresh
problem without copying the solution, explaining the invariant aloud, and
recording one failed approach or edge case. If a checkpoint is missed, spend
the next session on the weak area before adding breadth. Ask a peer or mock
interviewer to review the final design for trade-offs, scale, and failure
handling.

---

## Overview

This track gives you a solid foundation in data structures, algorithms, and system design fundamentals. By the end, you'll be prepared for phone screens and technical interviews.

### What You'll Learn
- Core data structures (arrays, strings, linked lists, trees, graphs)
- Essential algorithms (sorting, searching, dynamic programming)
- System design basics
- Common problem patterns and approaches

---

## Week 1: Foundations (Arrays & Strings)

**Time:** 10-12 hours  
**Focus:** Master basic data structures and manipulation techniques

### Arrays
- **Time:** 6-8 hours
- **Key Concepts:** Two pointers, sliding window, binary search
- **Domain:** [Arrays Domain](../domains/arrays.md)
- **Milestone:** Solve 3-4 array problems, understand two-pointers and sliding-window patterns

### Strings
- **Time:** 4-6 hours
- **Key Concepts:** Character manipulation, pattern matching, palindromes
- **Domain:** [Strings Domain](../domains/strings.md)
- **Milestone:** Solve 2-3 string problems, comfortable with basic transformations

### Weekly Checklist
- [ ] Complete easy array problems (start [here](../domains/arrays.md))
- [ ] Complete easy string problems
- [ ] Implement and test solutions in the maintained Python tree
- [ ] Review two-pointer and sliding-window patterns

### Week 1 Mastery Checkpoint

Before moving to Week 2, verify you can:

- [ ] Solve any two-pointer Easy problem in under 5 minutes
- [ ] Explain sliding window (fixed vs variable) with a concrete example
- [ ] Implement binary search correctly on the first try (no off-by-one)
- [ ] Name 3 ways to handle hash table collisions
- [ ] Recognize when to use a frequency map vs a sorted array for a lookup problem

**If any boxes are unchecked:** Re-study before proceeding.

| Weak area | Guide to revisit |
|-----------|-----------------|
| Two-pointer | [Two-Pointer Pattern](../../docs/07-patterns/two-pointer/README.md) |
| Sliding window | [Sliding Window Pattern](../../docs/07-patterns/sliding-window/README.md) |
| Binary search | [Binary Search Pattern](../../docs/07-patterns/binary-search/README.md) |
| Hash tables | [Hash Tables](../../docs/06-data-structures/hash-tables/README.md) |

---

## Week 2: Data Structures (Trees & Graphs)

**Time:** 10-12 hours  
**Focus:** Master hierarchical and network data structures

### Trees
- **Time:** 6-8 hours
- **Key Concepts:** DFS, BFS, binary search trees, tree traversals
- **Domain:** [Trees Domain](../domains/trees.md)
- **Milestone:** Solve 3-4 tree problems, understand DFS/BFS patterns

### Graphs
- **Time:** 4-6 hours
- **Key Concepts:** Graph representation, DFS, BFS, topological sort
- **Domain:** [Graphs Domain](../domains/graphs.md)
- **Milestone:** Solve 2-3 graph problems, comfortable with adjacency lists

### Weekly Checklist
- [ ] Complete easy tree problems (start [here](../domains/trees.md))
- [ ] Complete easy graph problems
- [ ] Implement and test solutions in the maintained Python tree
- [ ] Understand BFS vs DFS trade-offs

### Week 2 Mastery Checkpoint

Before moving to Week 3, verify you can:

- [ ] Traverse a binary tree iteratively (using a stack, not recursion) in all 3 orders
- [ ] Implement BST insert and search from scratch without notes
- [ ] Write BFS on a graph (adjacency list) and identify when BFS beats DFS
- [ ] Implement Union-Find with path compression
- [ ] Explain when to use a heap vs a BST for priority-based access

**If any boxes are unchecked:** Re-study before proceeding.

| Weak area | Guide to revisit |
|-----------|-----------------|
| Trees & traversals | [Trees](../../docs/06-data-structures/trees/README.md) |
| Binary search trees | [BST](../../docs/06-data-structures/trees/bst/README.md) |
| Graphs | [Graphs](../../docs/06-data-structures/graphs/README.md) |
| Union-Find | [DSU](../../docs/06-data-structures/dsu/README.md) |
| Heaps | [Heaps](../../docs/06-data-structures/heaps/README.md) |

---

## Week 3: Problem-Solving (DP & Sorting)

**Time:** 8-10 hours  
**Focus:** Master algorithmic problem-solving techniques

### Dynamic Programming
- **Time:** 5-6 hours
- **Key Concepts:** Memoization, tabulation, state definition
- **Domain:** [Dynamic Programming Domain](../domains/dynamic-programming.md)
- **Milestone:** Solve 2-3 DP problems, understand memoization patterns

### Sorting & Searching
- **Time:** 3-4 hours
- **Key Concepts:** Sort algorithms, binary search, search variations
- **Domain:** [Sorting & Searching Domain](../domains/sorting-searching.md)
- **Milestone:** Solve 1-2 problems, understand merge/quicksort/binary search

### Weekly Checklist
- [ ] Complete DP easy problems
- [ ] Complete sorting & searching easy problems
- [ ] Implement and test solutions in the maintained Python tree
- [ ] Review memoization approach

### Week 3 Mastery Checkpoint

Before moving to Week 4, verify you can:

- [ ] Solve 0/1 Knapsack with correct DP recurrence and bottom-up table
- [ ] Implement merge sort from scratch and derive its T(n) = 2T(n/2) + O(n) recurrence
- [ ] Explain memoization vs tabulation trade-offs (when to use each)
- [ ] Implement topological sort using DFS and identify when it applies
- [ ] Write binary search on a rotated sorted array without referencing the template

**If any boxes are unchecked:** Re-study before proceeding.

| Weak area | Guide to revisit |
|-----------|-----------------|
| Dynamic programming | [DP Algorithms](../../docs/05-algorithms/dp/README.md) |
| Sorting algorithms | [Sorting](../../docs/05-algorithms/sorting/README.md) |
| Graph algorithms | [Graph Algorithms](../../docs/05-algorithms/graphs/README.md) |
| Binary search | [Binary Search Pattern](../../docs/07-patterns/binary-search/README.md) |

---

## Week 4: System Design & Review

**Time:** 6-8 hours  
**Focus:** Learn system design basics and reinforce weak areas

### System Design Fundamentals
- **Time:** 3-4 hours
- **Key Concepts:** Caching, databases, scalability
- **Domain:** [System Design Fundamentals Domain](../domains/system-design-fundamentals.md)
- **Milestone:** Understand basic architecture patterns

### Review & Practice
- **Time:** 3-4 hours
- **Focus:** Revisit weak areas from weeks 1-3
- **Action:** Pick 2-3 hardest problems from previous weeks and re-solve

### Final Checklist
- [ ] Complete system design fundamentals (2-3 easy problems)
- [ ] Re-solve 2-3 hardest technical problems from weeks 1-3
- [ ] Write a summary of key patterns learned
- [ ] Do a mock interview (using [mock interviewer](../../AGENTS.md))

### Week 4 Mastery Checkpoint

Before calling yourself interview-ready, verify you can:

- [ ] Design a rate limiter with back-of-envelope math and data model in 20 minutes
- [ ] Explain CAP theorem in one sentence and give a real system example for both CP and AP
- [ ] Describe 3 cache invalidation strategies and when each is appropriate
- [ ] Complete a timed mock coding round (35 min) with a medium problem without hints
- [ ] Complete a timed mock system design round (45 min) without stopping

**If any boxes are unchecked:** Re-study before your interview.

| Weak area | Guide to revisit |
|-----------|-----------------|
| Rate limiter / system design | [Rate Limiter](../../docs/03-system-design/02-core-algorithms/rate-limiter.md) |
| Caching strategies | [LRU Cache](../../docs/03-system-design/01-caching/lru-cache.md) |
| Distributed systems | [Circuit Breaker](../../docs/03-system-design/08-infrastructure/circuit-breaker.md) |
| Mock interview | [Coding Good](../../docs/01-interview-frameworks/mock-transcripts/01-coding-good.md) |

---

## 📊 Problem Breakdown

| Domain | Easy | Medium | Hard | Total |
|--------|------|--------|------|-------|
| Arrays | 2 | 2 | - | 4 |
| Strings | 2 | 1 | - | 3 |
| Trees | 2 | 2 | - | 4 |
| Graphs | 1 | 2 | - | 3 |
| Dynamic Programming | 1 | 2 | - | 3 |
| Sorting & Searching | 2 | - | - | 2 |
| **Total** | **10** | **9** | **0** | **19** |

---

## Optional Practical-Labs Module

Use this module if you want a runnable systems exercise alongside the four-week
interview sequence. Choose one distributed-systems lab and one ML/AI lab; these
are small teaching models, not production services.

- [Distributed systems labs](../../docs/03-system-design/04-distributed-systems/README.md):
  practice quorum reads, consistent-hash partitioning, and rebalancing. Outcome:
  explain an invariant, a failure case, and the consistency/availability trade-off.
- [ML/AI systems labs](../../docs/04-ai-ml-llms/EDUCATIONAL_EXAMPLES.md): practice
  point-in-time features, RAG provenance, and guarded canary rollouts. Outcome:
  identify leakage, grounding, and promotion-safety checks.

Focused commands:

```bash
pytest tests/distributed_systems -q
pytest tests/ml_systems -q
```

The module is optional and does not change the stated 24-28 hour core-track estimate.

---

## 🚀 After Week 4

**Congrats!** You're ready for:
- ✅ Phone screen interviews
- ✅ Early technical rounds
- ✅ Basic system design questions

**Next steps:**
- Move to [8-Week Comprehensive](8-week-comprehensive.md) for deeper coverage
- Focus on your weakest domains using [Domains](../domains/)
- Practice with [mock interviewers](../../AGENTS.md)

---

## 📝 Tips for Success

1. **Code first:** Don't just read solutions — code every problem
2. **Test edge cases:** Always test with empty, single-element, and large inputs
3. **Time yourself:** Get comfortable solving under pressure
4. **Understand why:** Know why a solution works, not just how
5. **Track progress:** Mark problems complete as you go

---

## 🔗 Related Resources

- [All Domains](../domains/) — Deep dives
- [Interview Playbooks](../interview-playbooks/) — Stage-specific prep
- [Mock Interviewers](../../AGENTS.md) — Practice with AI
- [System Design](../../docs/03-system-design/README.md) — Full system design guide
