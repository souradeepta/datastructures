# InterviewPrep Project Specification

## Purpose

InterviewPrep is a practical study repository for software-development interviews. It combines
short explanations, interview frameworks, runnable Python implementations, tests, and time-boxed
learning paths. The project optimizes for clear practice loops: understand a technique, inspect or
write an implementation, run tests, and explain trade-offs aloud.

This is an educational repository, not a production library or a guarantee of interview questions
at any particular company.

## Users

- Intern and new-graduate candidates building algorithm fundamentals.
- Mid-level engineers practicing coding patterns, databases, and basic system design.
- Senior and staff candidates practicing architecture, RFCs, influence, and ambiguity.
- Interviewers and mentors who need exercises, examples, and discussion prompts.
- Contributors improving explanations, examples, tests, and navigation.

## Repository contract

1. `README.md`, `GETTING_STARTED.md`, `docs/INDEX.md`, and `docs/STRUCTURE.md` are visitor-facing
   entry points and must describe the current repository, not planned content as if it exists.
2. `docs/` contains guides and indexes. `learning-paths/` is a root-level directory for schedules
   and playbooks. Implementations live under `python/`, and maintained tests live under `tests/`.
3. Python examples should parse, import without unexpected side effects, and preserve their stated
   educational behavior when repaired or extended.
4. Documentation links in active Markdown must resolve to an existing repository path. Historical
   files under `docs/_archive/` are excluded from this requirement.
5. Claims about counts, language support, test coverage, and completion status must be verifiable
   from the repository or clearly labeled as goals.
6. New educational material should identify its audience, prerequisites where useful, complexity,
   edge cases, trade-offs, and at least one way to practice the idea.

## Quality gates

Run these commands from the repository root before submitting a change:

```bash
pytest -q
python3 scripts/validate_repo.py --imports
python3 scripts/audit_system_design.py \
  --max-structural-filler 27 \
  --max-copied-capacity 134
```

The validator uses only the Python standard library. It checks every Python source file under
`python/` for syntax errors and checks relative links in active Markdown while ignoring external
URLs, fenced code examples, and archived/internal planning material. With `--imports`, it also
imports each non-test implementation module without running its CLI example. A change that
intentionally adds an external or illustrative link should keep it outside the active-link contract
or document why it is not a repository path.

The current test suite is a tested core, not a claim that every educational module has dedicated
tests. New public implementations should add focused tests when practical.

CI runs these checks on Python 3.9 and 3.12 for pushes and pull requests. The system-design audit
reports known structural-filler and copied-capacity signatures grouped by topic and fails only
when either count exceeds its approved baseline. See the
[system-design content status](03-system-design/CONTENT_STATUS.md) for the current boundary and
the twenty focused system-design test groups. The [AI/ML lab status](04-ai-ml-llms/CONTENT_STATUS.md)
covers three additional ML-systems examples.

## Scope

### In scope

- Algorithm and data-structure explanations and Python implementations.
- Coding-pattern problem lists, walkthroughs, and tests.
- Database, system-design, AI/ML, and senior/staff interview preparation.
- Learning paths and mock-interview guidance.
- Lightweight validation and truthful navigation.

### Out of scope

- Production-ready distributed services or benchmark guarantees.
- Maintaining a Java implementation tree; Java references should not be presented as available
  unless that tree is added and tested.
- Treating the large system-design catalog as uniformly complete without a topic-level review.
- Rewriting archived material as part of routine maintenance.

## Prioritized roadmap

### P0 — Keep the core trustworthy — current status

- [x] Keep all Python files syntactically valid and run the validator in CI.
- [x] Keep visitor-facing links and repository counts accurate.
- [x] Add focused tests for selected high-use data-structure and system-design examples.
- [x] Add an audit boundary for known system-design content debt.

### P1 — Improve learning quality

- Replace placeholder sections and copied capacity calculations in active system-design guides with
  topic-specific examples, checked units, trade-off tables, and failure analysis.
- Add exercises and worked solutions to the algorithm and data-structure outlines.
- Add a consistent guide metadata convention to active long-form guides and validate it gradually.

### P2 — Improve contribution and automation — current status

- [x] Add CI that runs pytest, Python syntax validation, active Markdown link validation, and the
  system-design debt audit.
- Add formatter/linter configuration after agreeing on a style baseline.
- [x] Add contribution and security guidance.
- Select and add an explicit open-source license after maintainer decision.

### P3 — Expand deliberately

- [x] Add dependency-free distributed-systems and ML/AI-systems labs with focused tests,
  explicit contracts, and production-boundary documentation.
- Add Java only if there is a committed maintainer, build tool, tests, and documentation parity.
- Grow coverage based on learner demand and interview feedback rather than guide-count targets.

## Definition of done for a new guide

A new visitor-facing guide is ready when it has a clear audience and learning objective, links that
resolve, an accurate status/level statement, worked examples, complexity and trade-off discussion,
edge cases or failure modes, and a practical exercise. If implementation code is included, it must
parse and have either focused tests or an explicit explanation of why it is an illustrative snippet.
