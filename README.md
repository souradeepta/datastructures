# SDE Interview Prep

> Comprehensive interview preparation for engineers at all levels: intern through principal.
> 52 long-form study guides, 393 passing Python tests, 6 runnable systems labs, and 5 coding
> pattern libraries.

Maintainer context: [handoff](HANDOFF.md) · [memory and current decisions](MEMORY.md) ·
[project specification](docs/PROJECT_SPEC.md)

---

## I am preparing for...

### A FAANG/top-tier onsite in the next 2 weeks
→ [2-week sprint plan](learning-paths/sequential-tracks/2-week-sprint.md) + company-specific prep: [Google](learning-paths/company-specific/google-interview-prep.md) · [Meta](learning-paths/company-specific/meta-interview-prep.md) · [Amazon](learning-paths/company-specific/amazon-interview-prep.md) · [more](learning-paths/company-specific/)

### My first serious tech interview (new grad / intern)
→ [8-week comprehensive plan](learning-paths/sequential-tracks/8-week-comprehensive.md) — start with [coding patterns](docs/07-patterns/README.md) and [interview framework](docs/01-interview-frameworks/coding-interview-framework.md)

### A senior (L5) system design round
→ [System design playbook](learning-paths/interview-playbooks/system-design-round.md) + [database deep dives](docs/02-databases/) + [AI/ML systems](docs/04-ai-ml-llms/)

### A staff / principal (L6+) loop
→ [Senior/staff track](docs/09-senior-staff-track/) — RFC writing, ambiguity, cross-team influence, and bar-raiser prep

### Brushing up on a specific topic
→ [Master Index](docs/INDEX.md) — find any guide by level, topic, or time-to-read

---

## What's built

| Section | Status | What you get |
|---------|--------|--------------|
| [Databases](docs/02-databases/) | Study catalog | 30 long-form guides: SQL through distributed, sharding, consensus. |
| [AI/ML & LLMs](docs/04-ai-ml-llms/) | Study catalog + labs | 22 long-form guides plus 3 tested educational labs. |
| [Interview Frameworks](docs/01-interview-frameworks/) | Partial | 60 active guide files covering coding, system design, and behavioral rounds; needs exercises. |
| [Coding Patterns](docs/07-patterns/) | Active | Five pattern guides, problem lists, Python implementations, and tests. |
| [Data Structures](docs/06-data-structures/) | Active | Topic guides with implementation-oriented references. |
| [Algorithms](docs/02-algorithms/) | Active | Curated algorithm reference; `docs/05-algorithms/` provides focused indexes. |
| [System Design](docs/03-system-design/) | In progress | 705 active topic guides in 19 directories; 20 focused groups are tested, while broader review is ongoing. |

---

## Run the code

The Python test suite currently has 393 passing test cases, as collected by `pytest -q`, across
algorithms, data structures, distributed/ML systems, system-design examples, and 5 pattern
libraries. The six runnable labs are three distributed-systems labs and three ML/AI labs; each
has a focused implementation and test file:

```bash
git clone <repo>
cd datastructures
python3 -m pip install 'pytest>=8,<9'
pytest -q
python3 scripts/validate_repo.py --imports
```

Coding patterns: two-pointer · sliding window · binary search · monotonic stack · prefix sum

Run a single pattern:
```bash
pytest tests/patterns/test_two_pointer.py -v
```

---

## Learning paths

| Goal | Time | Path |
|------|------|------|
| Quick prep | 2 weeks | [2-week sprint](learning-paths/sequential-tracks/2-week-sprint.md) |
| Solid foundation | 4 weeks | [4-week focused](learning-paths/sequential-tracks/4-week-focused.md) |
| Deep mastery | 8 weeks | [8-week comprehensive](learning-paths/sequential-tracks/8-week-comprehensive.md) |
| By interview stage | — | [Phone screen](learning-paths/interview-playbooks/phone-screen.md) · [Technical round](learning-paths/interview-playbooks/technical-round.md) · [System design](learning-paths/interview-playbooks/system-design-round.md) |
| Company-specific | Varies | [Amazon](learning-paths/company-specific/amazon-interview-prep.md) · [Google](learning-paths/company-specific/google-interview-prep.md) · [Meta](learning-paths/company-specific/meta-interview-prep.md) · [more](learning-paths/company-specific/) |

---

## Mock interview agents

Practice with two AI-powered agents:
- **Interviewer Agent** — Asks questions, gives real-time feedback
- **Candidate Agent** — You ask it questions, it codes

See [AGENTS.md](AGENTS.md) for setup and usage.

---

## Stats

- **52** long-form study guides (30 database + 22 AI/ML; excludes section landing/status pages)
- **393** passing pytest test cases (the result of `pytest -q`)
- **6** runnable systems labs (3 distributed systems + 3 ML/AI), all with focused tests
- **5** coding pattern libraries (Python)
- **60** active interview framework guide files
- **7** topic sections
- **15** domain learning paths, plus schedule, playbook, company, and skill-tree paths

---

## FAQ

**Where do I start?**
Go to [GETTING_STARTED.md](GETTING_STARTED.md) and answer 3 quick questions. Takes 2 minutes.

**Can I just code without reading docs?**
Yes. Start with the pattern files in `python/patterns/` and run the tests. Learning happens by doing.

**Are these real interview problems?**
The repository uses common interview problems and patterns, including LeetCode-style exercises and
real-world design prompts. Coverage varies by section; run the linked tests to see what is
currently verified.

---

License pending maintainer selection. Usage and redistribution rights are not
granted by this repository notice until a license is added.
