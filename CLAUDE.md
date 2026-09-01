# CLAUDE.md — Collaboration Guidelines

This file documents how to work with Claude on the datastructures repository.

## Project Context

**Goal:** SDE interview preparation with 393 passing Python tests, five coding-pattern libraries,
six runnable distributed/ML systems labs, and a mix of reviewed, tested, and draft material.

**Repository Structure:** Topic-centric (docs/) with code implementations nested inside:
- `docs/01-interview-frameworks/` — 60 active interview-framework guide files
- `docs/02-databases/` — 30 long-form database guides
- `docs/03-system-design/` — 705 active topic guides across 19 directories, with focused tested examples
- `docs/04-ai-ml-llms/` — 22 long-form AI/ML guides plus 3 runnable labs
- `docs/05-algorithms/` — Algorithm implementations
- `docs/06-data-structures/` — Data structure implementations
- `docs/07-patterns/` — 5 coding-pattern libraries
- `learning-paths/` — Structured learning journeys

The maintained implementation and test trees are `python/` and `tests/`. The maintained Python
lab trees include `python/distributed_systems/` and `python/ml_systems/`. Java is not currently
part of the maintained repository contract.

## Content status vocabulary

- **Tested:** A focused automated test exercises the documented educational API. This does not
  establish production readiness.
- **Reviewed:** A maintainer has manually checked the objective, assumptions, calculations,
  trade-offs, failure modes, and links.
- **Draft:** Useful study material that has not passed the reviewed standard. Draft content may
  contain incomplete examples or calculations.

## Guide Frontmatter Convention

Every guide must include these lines immediately after the H1 title, with a blank line before the next content:

```
# Guide Title

**Level:** L4-L5
**Time to read:** ~20 min
**Prerequisites:** [Name](relative/path.md), ...  ← optional, omit if none
**Related:** [Name](relative/path.md), ...  ← optional
```

**Level definitions:**
- `L3` — intern / new grad (fundamentals)
- `L4` — mid-level (1-3 yrs, patterns + basic design)
- `L5` — senior (4-7 yrs, deep design, scale, trade-offs)
- `L5+` — staff (8+ yrs, cross-team, capacity planning, failure budgets)
- `L6+` — principal (multi-org, technical vision, strategy)

Use a range (e.g. `L3-L5`) when a guide spans multiple levels.

**Time to read estimates:**
- Short guides (<200 lines) → ~10 min
- Medium guides (200-500 lines) → ~20 min
- Long guides (500-1000 lines) → ~30 min
- Very long guides (1000+ lines) → ~45 min

**Prerequisites and Related:** Omit both lines unless the connection is obvious (e.g. `cap-theorem.md` as prerequisite for `distributed-databases.md`).

## Documentation Best Practices (Learned)

### Structure for Technical Guides

Each guide should include:

1. **Quick Summary** (50 words max)
   - What is it?
   - When to use?
   - Key benefit?

2. **Fundamentals** (Clear explanations)
   - Concepts with examples
   - Visual diagrams (ASCII art is fine)
   - Real-world analogies

3. **Trade-offs Section** (Critical!)
   - Feature comparison table
   - When to choose each option
   - Cost vs. performance graph
   - Consistency/availability trade-offs

4. **Architecture Patterns** (Diagrams + explanation)
   - ASCII diagrams showing flow
   - Real-world deployment patterns
   - Scaling strategies
   - Example: Master-Replica, Sharding, CQRS

5. **Interview Q&A** (Must-haves)
   - Start easy, progress to hard
   - Include common follow-ups
   - Explain "why" not just "what"
   - Real numbers and scenarios
   - Example: "Design for 1B users", "Handle failures"

6. **Practical Exercises** (With solutions!)
   - 4-5 exercises per guide
   - Easy → Medium → Hard progression
   - Complete working code/SQL
   - Real-world use cases
   - Explanation of trade-offs

### Content Depth

**Trade-offs > Length**
- Prefer focused trade-off analysis over generic comparisons
- Include specific numbers (latency, throughput, cost)
- Show when each option wins

**Diagrams > Words**
- ASCII diagrams for architecture
- Decision trees for "when to use"
- Comparison matrices instead of prose
- Performance graphs with axes

**Examples > Theory**
- Show complete working code
- Include sample data and output
- Demonstrate with real scenarios
- Real interview problems, not hypotheticals

**Exercises > Q&A**
- Move beyond questions to practical problems
- Provide solutions with explanations
- Progressive difficulty (Easy → Hard)
- Real-world scale (1M users, 1B events)

### How We Enhanced Database Section

**Phase 1: Trade-offs & Comparisons**
```
✓ Added comparison matrices (SQL vs. NoSQL, Columnar vs. Row-based)
✓ Included CAP theorem visualization
✓ Cost vs. performance graphs
✓ Decision frameworks (when to use each)
```

**Phase 2: Diagrams & Visualization**
```
✓ Architecture patterns (30+ ASCII diagrams)
✓ Data flow diagrams
✓ Compression technique examples
✓ Cardinality and scaling visualizations
```

**Phase 3: Interview Q&A**
```
✓ 5-10 comprehensive questions per guide
✓ Real-world scenarios (1M users, 1B events/day)
✓ Code examples and implementation details
✓ Performance analysis and optimization strategies
```

**Phase 4: Practical Exercises**
```
✓ 4-5 exercises per guide (21 total)
✓ Easy → Medium → Hard progression
✓ Complete working solutions (code/SQL)
✓ Real-world use cases and performance metrics
```

### Example: Good Database Guide Structure

```
# Topic Name

## ⚖️ Trade-offs Section
- Comparison table (features vs. cost vs. performance)
- When to use decision matrix
- Real numbers (latency, throughput, scale)

## 🏗️ Architecture Patterns
- Visual ASCII diagrams
- Real-world deployments
- Scaling strategies

## 📊 Comparison
- vs. competitors (side-by-side)
- Performance characteristics
- Use case matrix

## ❓ Interview Q&A
- 5-10 questions (easy → hard)
- Real scenarios
- Follow-ups
- Code examples

## 🧪 Practical Exercises
- 4-5 exercises
- Easy → Medium → Hard
- Complete solutions
- Trade-off analysis

## 💡 Interview Tips
- What interviewer is asking
- How to answer
- Key concepts
```

## Working Style Preferences

**One-Shot Execution**
- User prefers clear direction over planning
- Avoid lengthy "would you like me to..." questions
- Get to work quickly
- Report results, not process

**Concise Output**
- Terminal-focused feedback
- Focus on what changed
- Minimize verbosity
- Results over narration

**Practical Focus**
- Real code over theory
- Working examples over concepts
- Trade-off analysis over features
- Interview-ready content

## Communication Style

**With User:**
- Direct and concise
- Problem → Solution → Impact
- Avoid planning ceremonies
- Move fast

**In Code Comments:**
- None (well-named code is self-documenting)
- Only add if WHY is non-obvious
- No multi-paragraph docstrings
- No referencing issues/PRs

**In Documentation:**
- Examples first, explanation second
- Real numbers and metrics
- Decision trees when applicable
- "When to use" not "features"

## Git Practices

**Commit Style:**
- Descriptive commit messages
- Focus on "why" not "what"
- Batching related changes is OK
- One commit per logical unit

**Pushing:**
- Push after commits (don't hold changes)
- Use main branch (no unnecessary branching)
- Large changes OK if cohesive

## Content Quality Checklist

Before finishing a guide:

- [ ] **Trade-offs:** Included comparison table with real metrics
- [ ] **Diagrams:** At least 3 ASCII diagrams for complex topics
- [ ] **Q&A:** 5-10 questions spanning easy to hard
- [ ] **Exercises:** 4-5 practical exercises with solutions
- [ ] **Examples:** Real numbers (1M users, 1B events, etc.)
- [ ] **Performance:** Time/space complexity included
- [ ] **When-to-use:** Clear decision framework
- [ ] **Code:** Working solutions, not pseudocode
- [ ] **Trade-offs Explained:** Why each choice, not just how

## Section Completion Status

| Section | Status | Notes |
|---------|--------|-------|
| `docs/02-databases/` | 🟡 Study catalog | 30 long-form guides; review status varies |
| `docs/04-ai-ml-llms/` | 🟡 Study catalog + tested labs | 22 long-form guides and 3 tested labs |
| `docs/01-interview-frameworks/` | 🔲 Not expanded | 60 active guide files, needs exercises |
| `docs/03-system-design/` | 🟡 In progress | 705 topic guides; 20 focused tested groups; broader catalog remains draft/unreviewed |
| `docs/05-algorithms/` | 🔲 Not expanded | Needs trade-offs + complexity |
| `docs/06-data-structures/` | 🔲 Not expanded | Needs optimization examples |
| `docs/07-patterns/` | 🔲 Not expanded | 5 libraries, needs full solutions |
| `learning-paths/` | 🟡 Active | Time-based tracks, interview playbooks, and domain paths |

## For Future Work

**Database Guides Still Need:**
- Vector Databases: Add more exercises
- GraphQL: Add caching/performance exercises
- Data Warehousing: Add pipeline exercises
- Time-Series: Add cardinality management examples

**Next Priority Sections:**
- `docs/03-system-design/` — Add failure scenario exercises (highest interview value)
- `docs/07-patterns/` — Add complete solutions with complexity analysis
- `docs/05-algorithms/` — Add trade-off comparisons (BFS vs. DFS, Dijkstra vs. A*)
- `docs/06-data-structures/` — Add optimization examples and real-world use cases

**AI/ML Section Patterns (2026-05-23):**
- LLMOps: deployment cost models ($0.001/1K self-host vs $0.01/1K API), circuit breaker,
  canary deploy, semantic cache (40-60% cost reduction), model router (80% savings),
  Redis rate limiter, LLM-as-judge eval pipeline
- Multimodal: CLIP contrastive loss, LLaVA (ViT → MLP projection → LLM),
  Whisper (mel spectrogram → encoder-decoder), zero-shot CLIP, multimodal RAG with RRF

**Documentation Enhancement Potential:**
- Add video transcripts (mock interviews)
- Add whiteboard diagrams (real diagrams)
- Add code sandbox (interactive examples)
- Add community solutions (different approaches)

---

**Last Updated:** 2026-08-31
**Key Insight:** Trade-offs + Diagrams + Exercises support interview-ready study, but do not by
themselves establish that a guide is reviewed or production-ready.
