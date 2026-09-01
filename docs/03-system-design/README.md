# System Design Documentation

This is a broad system-design study catalog with 705 active topic-guide Markdown
files in 19 topic directories. This count excludes landing pages, status/index
pages, and nested README pages. The catalog is being reviewed incrementally;
individual guides should not be assumed to be reviewed, tested, or production-ready.

Start with the [content status and review boundary](CONTENT_STATUS.md). It
defines the repository’s `tested`, `reviewed`, and `draft` labels, records known
content debt, and identifies the twenty focused system-design test groups currently
backed by focused tests.

The [runnable educational examples](EDUCATIONAL_EXAMPLES.md) document the
contracts and limitations of the twenty focused test groups currently backed by
implementations and tests.

Maintainer context: [handoff](../../HANDOFF.md) · [memory and decisions](../../MEMORY.md) ·
[project specification](../PROJECT_SPEC.md)

## Topics

The catalog includes caching, core algorithms, design patterns, distributed
systems, real-world applications, data systems, social features, infrastructure,
storage and analytics, advanced algorithms and patterns, database internals,
real-world systems, ML recommendations, security, networking, containers,
messaging, and caching stores. Browse the directory list when choosing a topic;
the presence of a guide is not a review or test status claim.

For focused distributed-systems practice, start with the [distributed-systems
labs](04-distributed-systems/README.md) and [event-time streaming
lab](18-messaging-streaming/README.md). For ML/AI systems practice, use the
[AI/ML educational labs](../04-ai-ml-llms/EDUCATIONAL_EXAMPLES.md).

## Practice loop

1. Choose a guide and identify its stated requirements and assumptions.
2. Recalculate capacity numbers with explicit units and workload assumptions.
3. Compare trade-offs, failure handling, consistency, security, and cost.
4. Run or extend a focused implementation test where one exists.
5. Explain what would change at 10x scale and what remains unverified.

The repository quality boundary is enforced with
[`pytest`](../../pyproject.toml),
[`scripts/validate_repo.py`](../../scripts/validate_repo.py), and
[`scripts/audit_system_design.py`](../../scripts/audit_system_design.py).
