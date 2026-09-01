from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_documentation import (
    BATCH_2A_PATHS,
    BATCH_1_PATHS,
    batch_1_profile,
    batch_2a_profile,
    build_report,
    classify,
    main,
    parse_markdown,
)


def write_doc(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_active_boundary_and_categories(tmp_path: Path) -> None:
    write_doc(tmp_path, "docs/02-databases/topic.md", "# Topic\n\n## What it is\nIt is a thing.\n## Why it matters\nIt matters.\n")
    write_doc(tmp_path, "learning-paths/domains/sql.md", "# SQL\n")
    write_doc(tmp_path, "docs/_archive/old.md", "# Old\n")
    write_doc(tmp_path, "docs/00-resources/plan.md", "# Historical\n")

    report = build_report(tmp_path)

    assert report["active_markdown_files"] == 2
    assert report["section_counts"] == {"02-databases": 1, "learning-paths": 1}
    assert report["learning_path_category_counts"] == {"domains": 1}


def test_fenced_words_do_not_create_prose_signals() -> None:
    prose, fences, headings = parse_markdown(
        "# Example\n\n```python\n# What it is\n# Why it matters\nQ1: fake\n```\n"
    )

    assert "What it is" not in prose
    assert fences[0][0] == "python"
    assert headings == ["example"]


def test_unlabeled_fence_is_safe() -> None:
    prose, fences, _ = parse_markdown("# Example\n\n```\nWhat it is\n```\n")

    assert prose == "# Example\n"
    assert fences == [("", "What it is")]


def test_whole_repository_scan_is_a_regression_guard() -> None:
    root = Path(__file__).resolve().parents[1]

    report = build_report(root)

    assert report["active_markdown_files"] >= 1
    assert all("path" in item and "signals" in item for item in report["files"])


def test_classification_detects_required_signals(tmp_path: Path) -> None:
    content = """# Topic

## What it is
The mechanism.

## Why it matters
The workload.

## Trade-offs
| Choice | Advantage | Limitation |
|---|---|---|
| A | cheap | stale |
| B | fresh | costly |

```mermaid
flowchart LR
  A --> B
```

```python
print('example')
```

## Interview Q&A
Q1: What changes?\nA: State it.\nFollow-up: Why?\n
Q2: What fails?\nA: Recover it.\nFollow-up: How?\n
"""
    write_doc(tmp_path, "docs/02-databases/topic.md", content)

    item = classify(tmp_path / "docs/02-databases/topic.md", tmp_path)

    assert all(item["signals"][name] for name in ("what_why", "tradeoff_table", "mermaid", "code_example_fence", "qa"))
    assert item["signals"]["short_file"] is True
    assert item["short_file_status"] == "short"


def test_json_cli_is_machine_readable(tmp_path: Path, capsys) -> None:
    write_doc(tmp_path, "docs/topic.md", "# Topic\n")

    assert main(["--root", str(tmp_path), "--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["active_markdown_files"] == 1


def _valid_batch_1_doc() -> str:
    return """# Topic

**Level:** L4
**Status:** draft
**Audience:** Engineers
**Prerequisites:** keys
**Sequence:** Batch 1, 1/8
**Terra gate:** approved

## Learning objectives
- Explain the mechanism.
- Compare two choices.
- Diagnose a failure.

## What it is
The mechanism.

## Why it matters
The workload.

## Mental model
State and flow.

## Topic-specific visual
```mermaid
flowchart LR
  A[Source] --> B[Topic-specific sink]
```
The arrow shows the state transition and its bounded failure surface.

## Worked example
Assume 100 requests per second and a bounded result set.

## Advantages and limitations
| Choice | Advantage | Limitation |
|---|---|---|
| A | simple | limited |
| B | flexible | costly |

## Failure modes and operations
Measure lag and recover from a checkpoint.

## Practical exercises
1. Exercise one with an expected approach.
2. Exercise two with an expected approach.
3. Exercise three with an expected approach.
4. Exercise four with an expected approach.

## Interview Q&A
### Q1. What is it?
Answer. Follow-up: what fails?
### Q2. Why?
Answer. Follow-up: what changes?
### Q3. How is it measured?
Answer. Follow-up: which percentile?
### Q4. What is the trade-off?
Answer. Follow-up: at what scale?
### Q5. How does it recover?
Answer. Follow-up: what is durable?
### Q6. What is a bad fit?
Answer. Follow-up: which alternative?
### Q7. How do you migrate?
Answer. Follow-up: how do you roll back?
### Q8. What is the security boundary?
Answer. Follow-up: how is it tested?

## Related and next reading
- [SQL foundations](../02-databases/01-sql-advanced.md)
- [Operational replication](../02-databases/15-database-replication.md)
""" + "\n".join("Substantive detail for the foundational example." for _ in range(300))


def test_fail_on_missing_ignores_short_and_code_diagnostics(tmp_path: Path) -> None:
    write_doc(tmp_path, "docs/topic.md", """# Topic
## What it is
Definition.
## Why it matters
Reason.
## Trade-offs
| Choice | Advantage | Limitation |
|---|---|---|
| A | yes | no |
## Topic-specific visual
```mermaid
flowchart LR
A --> B
```
Explanation.
## Interview Q&A
Q1: question
Q2: question
""")

    assert main(["--root", str(tmp_path), "--fail-on-missing"]) == 0


def test_batch_1_profile_passes_all_rules(tmp_path: Path) -> None:
    path = tmp_path / BATCH_1_PATHS[0]
    path.parent.mkdir(parents=True)
    content = _valid_batch_1_doc()
    path.write_text(content, encoding="utf-8")
    item = classify(path, tmp_path)

    profile = batch_1_profile(item, content)

    assert profile["missing"] == []


def test_batch_2a_profile_passes_repository_guides() -> None:
    root = Path(__file__).resolve().parents[1]
    report = build_report(root, "batch-2a")

    assert report["profile_failure_messages"] == []
    assert {item["path"] for item in report["files"] if "batch_2a" in item} == set(BATCH_2A_PATHS)
    assert all(item["batch_2a"]["missing"] == [] for item in report["files"] if "batch_2a" in item)


def test_batch_2a_profile_reports_range_and_mode_rules(tmp_path: Path) -> None:
    path = tmp_path / BATCH_2A_PATHS[1]
    path.parent.mkdir(parents=True)
    content = _valid_batch_1_doc().replace("Batch 1, 1/8", "Batch 2A, 2/8").replace("approved", "open")
    content = content.replace("Substantive detail for the foundational example.", "")
    content += "\n".join("extra fixture line" for _ in range(100))
    path.write_text(content, encoding="utf-8")

    profile = batch_2a_profile(classify(path, tmp_path), content)

    assert {"line_range", "topic_requirements"}.issubset(profile["missing"])


def _valid_batch_2a_doc() -> str:
    content = """# Connection Pooling

**Level:** L4
**Status:** Reviewed (Terra PASS)
**Audience:** Engineers operating PostgreSQL services
**Prerequisites:** SQL, transactions, and basic queueing theory
**Sequence:** Batch 2A, 2/8
**Terra gate:** approved

## Learning objectives
- Explain pool sizing and queue behavior.
- Compare pooling modes and failure boundaries.
- Diagnose saturation with representative evidence.

## What it is
A connection pool bounds client-to-server database sessions.

## Why it matters
A queue can turn a service-time increase into checkout timeout and tail latency.

## Mental model
Arrival rate, service time, queue depth, reserved capacity, and per-instance limits determine throughput and overload behavior. Session pooling, transaction pooling, and statement pooling have different state and reset requirements; PgBouncer is one implementation.

## Topic-specific visual
```mermaid
flowchart LR
  Client[Clients] --> Pool[Pool]
  Pool --> Queue[Queue]
  Queue --> DB[Database]
```
The visual shows the bounded queue between clients and database sessions.

## Worked example
Assume a pool with a bounded queue, a checkout timeout, and a measured service time.

## Advantages and limitations
| Choice | Advantage | Limitation |
|---|---|---|
| Session pooling | Preserves session state | Consumes more connections |
| Transaction pooling | Higher reuse | Requires reset discipline |

## Failure modes and operations
Detect a connection leak, reset failure, failover, and queue growth with logs and metrics.

## Practical exercises
### Exercise 1: Size a pool
Use arrival rate and service time to estimate concurrency.
**Expected approach:** State assumptions, calculate a bound, and explain headroom.

### Exercise 2: Diagnose checkout timeout
Analyze a saturated pool and propose safe evidence collection.
**Expected approach:** Separate queue wait from database service time and identify a rollback trigger.

### Exercise 3: Choose a pooling mode
Compare session, transaction, and statement pooling for an application.
**Expected approach:** Check session state, reset behavior, failover, and operational ownership.

## Interview Q&A
### Q1. What is bounded?
**Answer:** The pool limits concurrent database sessions and may bound waiting clients.
**Follow-up:** Which queue metric predicts tail latency?

### Q2. Why can a larger pool hurt?
**Answer:** More sessions can increase database contention and memory use.
**Follow-up:** What evidence supports a resize?

### Q3. How do you detect a leak?
**Answer:** Correlate checked-out age, owner, and missing return events.
**Follow-up:** How do you prevent recurrence?

### Q4. When is transaction pooling useful?
**Answer:** It reuses sessions between transactions when session state is not required.
**Follow-up:** Which reset guarantees must hold?

### Q5. What happens during failover?
**Answer:** In-flight work may fail and idle connections must be recreated safely.
**Follow-up:** How should retries be bounded?

### Q6. How do you choose a timeout?
**Answer:** Derive it from the latency budget and distinguish queue from service time.
**Follow-up:** What is the rollback condition?

## Related and next reading
- [Query planning](17-query-planning.md)
- [Database monitoring](24-database-monitoring.md)
"""
    return content + "\n" + "\n".join(
        f"Fixture detail {index}: measure queueing, service time, and reset behavior under a declared workload."
        for index in range(240)
    )


def test_batch_2a_profile_requires_reviewed_approved_metadata(tmp_path: Path) -> None:
    path = tmp_path / BATCH_2A_PATHS[1]
    path.parent.mkdir(parents=True)
    content = _valid_batch_2a_doc()

    for status, gate in (("draft", "open"), ("reviewed", "approved"), ("Reviewed (Terra PASS)", "open")):
        broken = content.replace("**Status:** Reviewed (Terra PASS)", f"**Status:** {status}")
        broken = broken.replace("**Terra gate:** approved", f"**Terra gate:** {gate}")
        path.write_text(broken, encoding="utf-8")
        profile = batch_2a_profile(classify(path, tmp_path), broken)

        assert "metadata" in profile["missing"]


@pytest.mark.parametrize(
    ("rule", "mutate", "message"),
    [
            ("metadata", lambda text: text.replace("**Status:** Reviewed (Terra PASS)\n", "", 1), "add non-empty Level"),
        ("required_sections", lambda text: text.replace("## Mental model\n", "", 1), "restore all required sections"),
        (
            "topic_specific_visual",
            lambda text: text.replace(
                "```mermaid\nflowchart LR\n  Client[Clients] --> Pool[Pool]\n  Pool --> Queue[Queue]\n  Queue --> DB[Database]\n```\n",
                "",
                1,
            ),
            "topic-specific Mermaid visual",
        ),
        (
            "nearby_visual_explanation",
            lambda text: text.replace("The visual shows the bounded queue between clients and database sessions.\n", "", 1),
            "topic-specific Mermaid visual",
        ),
        (
            "table_count",
            lambda text: text.replace(
                "| Choice | Advantage | Limitation |\n|---|---|---|\n| Session pooling | Preserves session state | Consumes more connections |\n| Transaction pooling | Higher reuse | Requires reset discipline |\n\n",
                "",
                1,
            ),
            "add at least 1 Markdown comparison/trade-off table",
        ),
        ("exercise_guidance", lambda text: text.replace("**Expected approach:**", "**Discussion:**", 1), "missing solution or expected-approach guidance"),
        ("qa_answers", lambda text: text.replace("**Answer:**", "**Response:**", 1), "missing an Answer"),
        ("qa_followups", lambda text: text.replace("**Follow-up:**", "**Probe:**", 1), "missing a Follow-up"),
        ("cross_links", lambda text: text.replace("- [Database monitoring](24-database-monitoring.md)\n", "", 1), "add at least two Markdown links"),
    ],
    ids=["metadata", "required-sections", "visual", "visual-nearby", "table-count", "exercise-guidance", "qa-answer", "qa-follow-up", "cross-links"],
)
def test_batch_2a_strict_profile_rejects_one_mutated_rule(
    tmp_path: Path, capsys, rule: str, mutate, message: str
) -> None:
    path = tmp_path / BATCH_2A_PATHS[1]
    path.parent.mkdir(parents=True)
    broken = mutate(_valid_batch_2a_doc())
    path.write_text(broken, encoding="utf-8")

    profile = batch_2a_profile(classify(path, tmp_path), broken)

    expected_rule = "topic_specific_visual" if rule == "nearby_visual_explanation" else rule
    assert profile["missing"] == [expected_rule]
    assert main(["--root", str(tmp_path), "--profile", "batch-2a", "--fail-on-missing"]) == 1
    assert message in capsys.readouterr().out


def test_batch_2a_strict_profile_rejects_missing_required_paths(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--profile", "batch-2a", "--fail-on-missing"]) == 1

    output = capsys.readouterr().out
    assert BATCH_2A_PATHS[0] in output
    assert "required batch-2a guide is missing or empty; restore the file" in output


def test_batch_1_profile_reports_each_rule(tmp_path: Path) -> None:
    content = _valid_batch_1_doc()
    path = tmp_path / BATCH_1_PATHS[0]
    path.parent.mkdir(parents=True)
    path.write_text(content, encoding="utf-8")
    replacements = {
        "metadata": "**Level:** L4",
        "objectives_count": "- Explain the mechanism.",
        "foundational_line_floor": "Substantive detail for the foundational example.",
        "topic_specific_visual": "## Topic-specific visual",
        "tradeoff_table": "| Choice | Advantage | Limitation |",
        "worked_example": "## Worked example",
        "exercise_count": "1. Exercise one with an expected approach.",
        "qa_count": "### Q1. What is it?",
        "exercise_guidance": "1. Exercise one with an expected approach.",
        "qa_answers": "Answer.",
        "qa_followups": "Follow-up:",
        "sequence": "**Sequence:** Batch 1, 1/8",
        "terra_gate": "**Terra gate:** approved",
        "cross_links": "- [SQL foundations](../02-databases/01-sql-advanced.md)",
    }
    for rule, marker in replacements.items():
        if rule == "foundational_line_floor":
            broken = content.split("Substantive detail", 1)[0]
        elif rule == "exercise_guidance":
            broken = content.replace(marker, "1. Exercise one.", 1)
        elif rule == "qa_answers":
            broken = content.replace(marker, "Response.", 1)
        elif rule == "qa_followups":
            broken = content.replace(marker, "Probe:", 1)
        else:
            broken = content.replace(marker, "", 1)
        path.write_text(broken, encoding="utf-8")
        item = classify(path, tmp_path)
        profile = batch_1_profile(item, broken)
        assert rule in profile["missing"], rule
        if rule == "exercise_guidance":
            assert any("Exercise 1" in message and "expected-approach" in message for message in profile["failure_messages"])
        elif rule == "qa_answers":
            assert any("missing an Answer" in message for message in profile["failure_messages"])
        elif rule == "qa_followups":
            assert any("missing a Follow-up" in message for message in profile["failure_messages"])

    for mode in ("missing", "empty"):
        isolated_root = tmp_path / mode
        if mode == "empty":
            write_doc(isolated_root, BATCH_1_PATHS[0], "")
        report = build_report(isolated_root, profile="batch-1")
        assert BATCH_1_PATHS[0] in report["profile_missing_paths"]
        assert main(["--root", str(isolated_root), "--profile", "batch-1", "--fail-on-missing"]) == 1
