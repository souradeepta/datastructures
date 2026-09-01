# Getting Started — Find Your Path in 2 Minutes

Welcome to **InterviewPrep**! You're here to prep for SDE interviews. We'll help you find the right learning path for your situation.

Answer 3 quick questions below — there are no wrong answers. We'll route you to resources tailored to your timeline, interview stage, and learning style.

---

## Answer 3 Quick Questions

### Q1: How much time do you have until your interview?

- **2 weeks** — Intensive, focused sprint
- **4 weeks** — Balanced, recommended (most popular)
- **8 weeks** — Comprehensive, deep dive

### Q2: What's your current interview stage?

- **Phone screen / Coding challenges** — Mainly algorithms & data structures
- **Technical round** — Medium-hard coding problems, system fundamentals
- **System design round** — Architecture, trade-offs, scaling
- **Not sure yet** — Show me all paths

### Q3: How do you learn best?

- **Step-by-step guidance** — Read frameworks first, then implement
- **Dive deep** — Master each topic thoroughly before moving on
- **Learn by doing** — Code first, understand after; tests guide you

---

## Your Personalized Path

Based on your answers above, here are curated resources for your learning journey:

### Sample Paths (customize based on your answers):

#### Path 1: "4-Week Balanced Technical Interview Path"
*For: 4 weeks, Technical round, Step-by-step learning*

**Estimated Commitment:** 24-28 hours over 4 weeks (6-7 hours/week)

**What You'll Master:**
- Core coding interview frameworks and patterns
- 40+ algorithm problems organized by pattern
- Practice with real test cases (393 tests in the repo)

**Week-by-Week Breakdown:**

**Week 1: Coding Fundamentals & Frameworks**
- Read: [Coding Interview Framework](docs/01-interview-frameworks/coding-interview-framework.md)
- Code: Start with [Two-Pointer Pattern](python/patterns/two_pointer.py) — 10 foundational problems
- Tests: Run `pytest tests/patterns/test_two_pointer.py -v` to see all tests pass
- Commit: Write your own solutions, compare with repo

**Week 2: Core Algorithms & Patterns**
- Read: [Two-Pointer Techniques](docs/01-interview-frameworks/two-pointer-techniques.md)
- Code: Practice [Sliding Window](python/patterns/sliding_window.py) (9 problems) and [Binary Search](python/patterns/binary_search.py) (8 problems)
- Tests: Run all pattern tests to verify solutions
- Interview Practice: Start with [AGENTS.md](AGENTS.md) — schedule a practice round

**Week 3: Data Structures & Problem-Solving**
- Read: [Data Structures](docs/06-data-structures/README.md)
- Code: Implement [Monotonic Stack](python/patterns/monotonic_stack.py) (6 problems) and [Prefix Sum](python/patterns/prefix_sum.py) (6 problems)
- Tests: Verify your implementations with `pytest tests/patterns/ -v`
- Reflection: Review mistakes, understand trade-offs

**Week 4: Integration & Mock Interviews**
- Review: Re-solve your 5 toughest problems from weeks 1-3
- Practice: 2-3 mock interviews with agents ([AGENTS.md](AGENTS.md))
- Stretch: Read System Design basics ([System Design Guide](docs/01-interview-frameworks/system-design-interview-guide.md))

**Your Resources:**
- 📖 **Frameworks & Guides:** [docs/01-interview-frameworks/](docs/01-interview-frameworks/)
- 💻 **Code Examples:** [python/patterns/](python/patterns/) (five pattern libraries with focused tests)
- 🧪 **Run Tests:** `pytest tests/patterns/ -v` to verify all solutions
- 🤖 **Mock Interviews:** [AGENTS.md](AGENTS.md) — live practice with Claude interviewer

**Next Step:** [Jump to Mock Interviews →](AGENTS.md)

---

#### Path 2: "2-Week Intensive Phone Screen Sprint"
*For: 2 weeks, Phone screen, Learn-by-doing*

**Estimated Commitment:** 20 hours over 2 weeks (10 hours/week)

**What You'll Master:** Rapid problem-solving, quick pattern recognition, coding speed

**Week 1: Patterns & Problems (10 hours)**
- Dive into [Two-Pointer](python/patterns/two_pointer.py) and [Sliding Window](python/patterns/sliding_window.py)
- Run `pytest tests/patterns/test_two_pointer.py tests/patterns/test_sliding_window.py -v`
- Solve each problem, study test cases to understand the expected input/output

**Week 2: Speed & Mock Interviews (10 hours)**
- Daily: Solve 3-5 problems from [Binary Search](python/patterns/binary_search.py)
- Schedule 3 mock interviews via [AGENTS.md](AGENTS.md)
- Analyze feedback, refine approach

---

#### Path 3: "8-Week System Design Mastery"
*For: 8 weeks, System design, Dive deep*

**Estimated Commitment:** 32-40 hours over 8 weeks (4-5 hours/week)

**What You'll Master:** Architecture patterns, trade-offs, real-world systems, scale

**Overview:**
- Weeks 1-2: [System Design Fundamentals](docs/01-interview-frameworks/system-design-interview-guide.md)
- Weeks 3-4: [Caching Strategies](docs/03-system-design/01-caching/)
- Weeks 5-6: [Real-World Case Studies](docs/03-system-design/)
- Weeks 7-8: [Mock Interviews](AGENTS.md) + Refinement

---

### Other Learning Paths

**Can't find your exact combo above?** No problem:

- **All 2-week paths** → Search for "2-week" on this page or [STRUCTURE.md](docs/STRUCTURE.md)
- **All 4-week paths** → [Learning Paths Index](learning-paths/)
- **All 8-week paths** → [Comprehensive Tracks](learning-paths/sequential-tracks/8-week-comprehensive.md)
- **Specialty paths** (breadth-first, depth-first) → [Learning Styles](learning-paths/skill-trees/)

---

## Not Sure Which Path Fits You?

No problem! Here are some quick alternatives:

**Option A: Explore the Repo**
→ Jump to [docs/STRUCTURE.md](docs/STRUCTURE.md) for a visual map of everything

**Option B: Jump Straight to Code**
→ Start with [python/patterns/](python/patterns/) and run tests
```bash
cd /home/sbisw/github/datastructures
pytest tests/patterns/test_two_pointer.py -v
```

**Option C: Practice Interviews Now**
→ [AGENTS.md](AGENTS.md) — Schedule a live mock interview

**Option D: Learn the Process First**
→ [Coding Interview Framework](docs/01-interview-frameworks/coding-interview-framework.md) (20-minute read)

---

## Quick Stats

- **393 passing Python tests** across algorithms, data structures, distributed/ML systems, system-design examples, and patterns
- **40+ interview pattern problems** organized by technique
- **50+ framework guides** covering coding, system design, and behavioral interviews
- **9 learning paths** for different timelines and goals
- **2 mock interview agents** for real-time practice
- **Python implementations** with a tested core and additional educational examples

---

## FAQ

**Q: I don't know my timeline. What should I pick?**  
A: Pick 4 weeks. It's the most flexible and allows deep learning without overwhelming yourself.

**Q: Can I switch paths after starting?**  
A: Absolutely. All patterns and frameworks are independent. Jump between them freely.

**Q: What if I just want to code?**  
A: Go to [python/patterns/](python/patterns/), pick a topic, and run the tests. Learning happens by solving.

**Q: How much time should I spend on each problem?**  
A: Try solving for 15-20 minutes first. If stuck, check the test file to understand the expected behavior, then try again.

---

## Ready? Pick Your Path Above & Start!

Questions? Check [docs/STRUCTURE.md](docs/STRUCTURE.md) for the full repo map.

Good luck! You've got this. 🚀
