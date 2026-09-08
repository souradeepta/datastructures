from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scripts.audit_documentation import (
    BATCH_2B_PATHS,
    BATCH_2B_RULES,
    BATCH_2A_PATHS,
    BATCH_1_PATHS,
    batch_1_profile,
    batch_2c_profile,
    batch_2b_profile,
    batch_2a_profile,
    build_report,
    classify,
    explained_mermaid_count,
    has_bounded_term,
    main,
    parse_markdown,
)
from scripts.documentation_profile_definitions import (
    BATCH_2C_PATHS,
    BATCH_3A_PATHS,
    BATCH_4A_PATHS,
    BATCH_5_PATHS,
    ESTABLISHED_PROFILES,
    FUTURE_PROFILES,
    PROFILE_DEFINITIONS,
)


def _valid_batch_2b_optimization_doc() -> str:
    content = """# Time-Series Optimization

**Level:** L4–L5 focused companion
**Status:** draft
**Audience:** Engineers optimizing a metrics TSDB
**Prerequisites:** time-series databases, SQL, and SLOs
**Sequence:** Batch 2B, 4/8
**Terra gate:** open

## Learning objectives
- Calculate chunk, rollup, tier, and retention capacity from stated units.
- Compare raw fidelity with downsampling and compression.
- Diagnose late data, compaction, and DST failures against an SLO.

## What it is
Chunks, compression, rollup, tier, raw, fidelity, hot, warm, and cold storage
are physical choices for a time-series system. Provider and version behavior
must be checked before using an optimization setting.

## Why it matters
An SLO balances storage cost and query work. Raw data preserves fidelity while
downsampling reduces bytes; late data can revise a rollup.

## Mental model
Raw samples enter chunks, compression reduces physical bytes, a watermark closes
rollups, and tier movement copies validated data. Compaction rewrites files.

## Worked example
Assume 100,000 series at one sample every 15 seconds. Samples/day are
`100,000 * 86,400 / 15 = 576,000,000`. At 2.4 compressed bytes/sample,
seven-day raw storage is 9.6768 GB decimal before replicas and WAL. A 60-second
rollup has 144 million rows/day. The dashboard SLO is p95 under 2 seconds and
the ingest SLO is 99.9% visible within 60 seconds. Use raw for the newest
watermark boundary and rollups for closed buckets.

## Advantages and limitations
| Representation | Fidelity | Query use | Limitation |
| --- | --- | --- | --- |
| Raw | Exact | Forensics | Higher storage and scan work |
| Rollup | Summary | Long dashboards | Loses spikes and exact order |
| Cold archive | Exact if raw | Rare restore | Higher retrieval time |

| Policy | Storage | Query | Operational trade-off |
| --- | --- | --- | --- |
| Raw 30 days | Highest | Exact | Simple correction |
| Raw 7 days plus rollup | Lower | Fast trends | Requires late correction |
| Hourly only | Lowest | Coarse | Forensics lost |

## Topic-specific visual
```mermaid
flowchart LR
  Raw[Raw samples] --> Watermark[Watermark]
  Watermark --> Rollup[Rollup]
  Rollup --> Warm[Warm tier]
  Raw --> Hot[Hot tier]
  Late[Late data] --> Correction[Late correction]
  Correction --> Rollup
```
The raw-to-rollup diagram shows that late data corrects a closed bucket only
through a durable correction path.

```mermaid
sequenceDiagram
  Query->>Router: Range query
  Router->>Rollup: Closed buckets
  Router->>Raw: Open boundary
  Raw-->>Router: Exact values
  Rollup-->>Router: Summary and watermark
```
The query path keeps recent exact data separate from summarized history and
reports the fidelity boundary.

## Failure modes and operations
Monitor downsampling error, chunk count, compaction lag, tier copy checksums,
late-data age, and SLO burn. DST can create a 23- or 25-hour civil day; use UTC
for fixed windows. Retain raw through the correction window, validate copies,
and replay idempotently. Provider/version caveats apply to compression and
out-of-order behavior.

## Practical exercises
### Exercise 1: Size retention
Calculate raw bytes and compare a rollup policy.
**Expected approach:** Multiply series, samples per second, seconds/day, and
bytes/sample; state decimal versus binary units, replicas, and fidelity loss.

### Exercise 2: Correct late data
Repair a sample arriving after the rollup watermark.
**Solution:** Recompute the affected raw bucket and parent rollup using a stable
sample identity, publish a new version, and retain the prior snapshot for rollback.

### Exercise 3: Protect the ingest SLO
Compaction raises p99 ingest beyond the 60-second SLO.
**Expected approach:** Throttle compaction, preserve raw writes, track debt, and
resume only below an abort threshold after measuring query/storage benefit.

## Interview Q&A
### Q1. What does compression change?
**Answer:** It changes physical bytes and CPU, not raw semantics; measured ratios
depend on data distribution and provider version.
**Follow-up:** Which workload slice would you benchmark?
### Q2. Can averages be averaged?
**Answer:** Merge sums and counts, then divide; unweighted bucket averages can be wrong.
**Follow-up:** How do you merge quantiles?
### Q3. Why keep raw data?
**Answer:** Raw preserves spike and late-correction fidelity that a rollup cannot reconstruct.
**Follow-up:** What closes the correction window?
### Q4. How do tiers affect an SLO?
**Answer:** Cold storage can reduce cost while adding retrieval latency and restore work.
**Follow-up:** Which query class may use cold data?
### Q5. How do you handle DST?
**Answer:** Use UTC fixed windows or explicitly model civil days with timezone rules and version.
**Follow-up:** Which timezone database produced the report?
### Q6. What is a safe compaction rollout?
**Answer:** Validate a new snapshot, checksum and compare aggregates, then publish and retain rollback data.
**Follow-up:** What is the abort condition?

## Related and next reading
- [Time-series databases](05-timeseries-databases.md)
- [Columnar databases](04-columnar-databases.md)
"""
    return content + "\n" + "\n".join(
        f"Review note {index}: retain explicit units, versions, fidelity, and recovery evidence."
        for index in range(330)
    )


def write_doc(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_batch_2b_fixture(root: Path, content: str | None = None) -> tuple[Path, str]:
    """Write the focused Batch 2B fixture and its two valid local links."""
    relative = BATCH_2B_PATHS[3]
    fixture = content or _valid_batch_2b_optimization_doc()
    write_doc(root, relative, fixture)
    write_doc(root, "docs/02-databases/05-timeseries-databases.md", "# Related\n")
    write_doc(root, "docs/02-databases/04-columnar-databases.md", "# Related\n")
    return root / relative, fixture


def write_batch_2c_fixture(root: Path, relative: str, content: str | None = None) -> tuple[Path, str]:
    """Copy a real Batch 2C guide into an isolated root with valid local links."""
    source_root = Path(__file__).resolve().parents[1]
    fixture = content or (source_root / relative).read_text(encoding="utf-8")
    fixture = fixture.split("## Related and next reading", 1)[0] + """## Related and next reading
- [Related one](related-one.md)
- [Related two](related-two.md)
- [Related three](related-three.md)
"""
    write_doc(root, relative, fixture)
    for name in ("related-one.md", "related-two.md", "related-three.md"):
        write_doc(root, str(Path(relative).parent / name), "# Related\n")
    return root / relative, fixture


def test_batch_2b_profile_covers_exact_paths_and_passes_repository_guides() -> None:
    root = Path(__file__).resolve().parents[1]
    report = build_report(root, "batch-2b")
    profile_items = [item for item in report["files"] if "batch_2b" in item]

    assert len(profile_items) == 8
    assert {item["path"] for item in profile_items} == set(BATCH_2B_PATHS)
    assert report["profile_failure_messages"] == []
    assert all(item["batch_2b"]["missing"] == [] for item in profile_items)


@pytest.mark.parametrize(("status", "gate"), [("draft", "open"), ("reviewed", "approved")])
def test_batch_2b_profile_accepts_implementation_and_final_metadata_states(
    tmp_path: Path, status: str, gate: str
) -> None:
    content = _valid_batch_2b_optimization_doc()
    content = content.replace("**Status:** draft", f"**Status:** {status}")
    content = content.replace("**Terra gate:** open", f"**Terra gate:** {gate}")
    path, _ = write_batch_2b_fixture(tmp_path, content)

    profile = batch_2b_profile(classify(path, tmp_path), content, tmp_path)

    assert profile["missing"] == []


@pytest.mark.parametrize(("status", "gate"), [("draft", "approved"), ("reviewed", "open")])
def test_batch_2b_profile_rejects_mismatched_metadata_states(
    tmp_path: Path, status: str, gate: str
) -> None:
    content = _valid_batch_2b_optimization_doc()
    content = content.replace("**Status:** draft", f"**Status:** {status}")
    content = content.replace("**Terra gate:** open", f"**Terra gate:** {gate}")
    path, _ = write_batch_2b_fixture(tmp_path, content)

    profile = batch_2b_profile(classify(path, tmp_path), content, tmp_path)

    assert profile["missing"] == ["metadata"]


@pytest.mark.parametrize(("duplicate_status", "duplicate_gate"), [("draft", "approved"), ("reviewed", "open")])
def test_batch_2b_profile_rejects_duplicate_conflicting_metadata(
    tmp_path: Path, duplicate_status: str, duplicate_gate: str
) -> None:
    content = _valid_batch_2b_optimization_doc()
    content = content.replace("**Status:** draft", "**Status:** reviewed")
    content = content.replace("**Terra gate:** open", "**Terra gate:** approved")
    content += f"\n**Status:** {duplicate_status}\n**Terra gate:** {duplicate_gate}\n"
    path, _ = write_batch_2b_fixture(tmp_path, content)

    profile = batch_2b_profile(classify(path, tmp_path), content, tmp_path)

    assert profile["missing"] == ["metadata"]


@pytest.mark.parametrize(
    ("rule", "mutate"),
    [
        ("metadata", lambda text: text.replace("**Status:** draft\n", "", 1)),
        (
            "line_range",
            lambda text: text + "\n" + "\n".join("extra line" for _ in range(100)),
        ),
        ("required_sections", lambda text: text.replace("## Mental model\n", "", 1)),
        (
            "mermaid_count",
            lambda text: text.replace(
                "The raw-to-rollup diagram shows that late data corrects a closed bucket only\nthrough a durable correction path.\n\n",
                "",
                1,
            ).replace(
                "The query path keeps recent exact data separate from summarized history and\nreports the fidelity boundary.\n\n",
                "",
                1,
            ),
        ),
        (
            "exercise_guidance",
            lambda text: text.replace("**Expected approach:**", "**Discussion:**", 1),
        ),
        ("qa_answers", lambda text: text.replace("**Answer:**", "**Response:**", 1)),
        (
            "related_links",
            lambda text: text.replace("- [Columnar databases](04-columnar-databases.md)\n", "", 1),
        ),
        (
            "topic_requirements",
            lambda text: __import__("re").sub("provider", "backend", text, flags=__import__("re").I),
        ),
    ],
    ids=[
        "metadata",
        "line-range",
        "required-headings",
        "mermaid-explanations",
        "exercises",
        "qa",
        "links",
        "topic-requirements",
    ],
)
def test_batch_2b_profile_rejects_one_mutated_rule(
    tmp_path: Path, capsys, rule: str, mutate
) -> None:
    path, _ = write_batch_2b_fixture(tmp_path, mutate(_valid_batch_2b_optimization_doc()))
    content = path.read_text(encoding="utf-8")
    profile = batch_2b_profile(classify(path, tmp_path), content, tmp_path)

    assert profile["missing"] == [rule]
    assert main(["--root", str(tmp_path), "--profile", "batch-2b", "--fail-on-missing"]) == 1
    assert rule in capsys.readouterr().out


def test_batch_2b_profile_rejects_missing_required_paths(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--profile", "batch-2b", "--fail-on-missing"]) == 1

    output = capsys.readouterr().out
    assert len(BATCH_2B_PATHS) == 8
    assert all(path in output for path in BATCH_2B_PATHS)
    assert "required batch-2b guide is missing or empty; restore the file" in output


def test_profile_registry_preserves_established_and_open_cohorts() -> None:
    assert ESTABLISHED_PROFILES == ("batch-1", "batch-2a", "batch-2b")
    assert set(FUTURE_PROFILES) == {"batch-2c", "batch-3a", "batch-4a", "batch-5"}
    assert all(PROFILE_DEFINITIONS[name].enabled for name in ESTABLISHED_PROFILES)
    assert all(not PROFILE_DEFINITIONS[name].enabled for name in FUTURE_PROFILES)
    assert BATCH_2C_PATHS == (
        "docs/02-databases/13-consensus-algorithms.md",
        "docs/02-databases/22-distributed-tracing.md",
        "docs/02-databases/30-stream-processing.md",
    )
    assert len(BATCH_3A_PATHS) == 5
    assert len(BATCH_4A_PATHS) == 4
    assert len(BATCH_5_PATHS) == 3


@pytest.mark.parametrize("profile", ("batch-3a", "batch-4a", "batch-5"))
def test_open_profile_scaffold_is_non_blocking_and_reports_paths(tmp_path: Path, profile: str, capsys) -> None:
    report = build_report(tmp_path, profile)

    definition = PROFILE_DEFINITIONS[profile]
    assert report["profile_status"] == "open"
    assert report["profile_enabled"] is False
    assert report["profile_paths"] == list(definition.paths)
    assert report["profile_missing_paths"] == list(definition.paths)
    assert main(["--root", str(tmp_path), "--profile", profile, "--fail-on-missing"]) == 0
    assert "Profile:" in capsys.readouterr().out


def test_future_profile_path_is_checked_when_present_but_not_structurally_enforced(tmp_path: Path) -> None:
    path = tmp_path / BATCH_2C_PATHS[0]
    path.parent.mkdir(parents=True)
    path.write_text("# Open future guide\n", encoding="utf-8")

    report = build_report(tmp_path, "batch-2c")
    item = next(item for item in report["files"] if item["path"] == BATCH_2C_PATHS[0])

    assert item["batch_2c"]["missing"]
    assert BATCH_2C_PATHS[0] not in report["profile_missing_paths"]
    assert main(["--root", str(tmp_path), "--profile", "batch-2c", "--fail-on-missing"]) == 1


def test_batch_2c_profile_is_strict_locally_but_not_ci_enabled() -> None:
    root = Path(__file__).resolve().parents[1]
    report = build_report(root, "batch-2c")
    profile_items = [item for item in report["files"] if "batch_2c" in item]

    assert len(profile_items) == 3
    assert report["profile_status"] == "open"
    assert report["profile_enabled"] is False
    assert PROFILE_DEFINITIONS["batch-2c"].strict is True
    assert report["profile_failure_messages"] == []
    assert all(item["batch_2c"]["missing"] == [] for item in profile_items)
    assert main(["--profile", "batch-2c", "--fail-on-missing"]) == 0


def test_batch_2c_profile_rejects_arbitrary_content_for_every_required_path(tmp_path: Path, capsys) -> None:
    for relative in BATCH_2C_PATHS:
        write_doc(tmp_path, relative, "# Arbitrary note\n\nThis is not a guide.\n")

    report = build_report(tmp_path, "batch-2c")
    profile_items = [item for item in report["files"] if "batch_2c" in item]

    assert len(profile_items) == 3
    assert all(item["batch_2c"]["missing"] for item in profile_items)
    assert main(["--root", str(tmp_path), "--profile", "batch-2c", "--fail-on-missing"]) == 1
    output = capsys.readouterr().out
    assert "required_sections" in output
    assert "line_range" in output


@pytest.mark.parametrize(
    ("rule", "mutate"),
    [
        ("metadata", lambda text: text.replace("**Status:** reviewed\n", "**Status:** reviewed (pending)\n", 1)),
        ("objectives_count", lambda text: text.replace("- Diagnose quorum loss, stale leaders, uncommitted current-term entries, and unsafe recovery decisions.\n", "", 1).replace("- Compare Raft, Paxos, and BFT for a database with explicit latency, membership, and trust constraints.\n", "", 1).replace("- Explain why safety and liveness are different claims, and identify the assumptions each protocol needs.\n", "", 1)),
        ("line_range", lambda text: text + "\n" + "\n".join("extra fixture line" for _ in range(200))),
        ("required_sections", lambda text: text.replace("## Mental model\n", "", 1)),
        ("topic_requirements", lambda text: re.sub(r"\bRaft\b", "protocol", text, flags=re.I)),
        (
            "mermaid_count",
            lambda text: text.replace(
                "The important edge is not merely “candidate becomes leader.” The candidate wins\nonly with a quorum and a sufficiently current log; the new leader then proves\nauthority with heartbeats and waits for durable acknowledgements from both D and\nE. In this trace C+D+E=3/5 is the point where `commit_index` may advance, the\nstate machine may apply, and the client may receive success. A two-node minority\ncannot take the same safe path in a five-voter configuration.\n\n",
                "",
                1,
            ).replace(
                "The `prev index/term` check is the log-matching guard; a durable quorum\nacknowledgement is the commit evidence. A linearizable read waits for a\nquorum-confirmed leader and local application through the read index. A\nsnapshot replaces only a compacted prefix and must itself be durable before the\nold prefix is discarded.\n\n",
                "",
                1,
            ),
        ),
        (
            "table_count",
            lambda text: re.sub(r"\| Protocol family \|.*?\n\| BFT \|.*?\n\n", "", re.sub(
                r"\| Fault model \|.*?\n\| Read-only witness \|.*?\n\n", "", text, count=1, flags=re.S
            ), count=1, flags=re.S),
        ),
        (
            "exercise_count",
            lambda text: re.sub(r"### Exercise 4:.*?(?=## Interview Q&A)", "", text, count=1, flags=re.S),
        ),
        ("exercise_guidance", lambda text: text.replace("**Solution / expected approach:**", "**Discussion:**", 1)),
        ("qa_count", lambda text: re.sub(r"### Q8\..*?(?=## Related and next reading)", "", text, count=1, flags=re.S)),
        ("qa_answers", lambda text: text.replace("**Answer:**", "**Response:**", 1)),
        ("qa_followups", lambda text: text.replace("**Follow-up:**", "**Probe:**", 1)),
        ("related_links", lambda text: text.replace("related-three.md", "missing-related.md", 1)),
    ],
    ids=[
        "metadata", "objectives", "line-range", "required-sections", "topic-terms",
        "diagram-explanation", "tables", "exercise-count", "exercise-guidance",
        "qa-count", "qa-answers", "qa-followups", "broken-local-link",
    ],
)
def test_batch_2c_profile_rejects_each_requirement(tmp_path: Path, capsys, rule: str, mutate) -> None:
    path, fixture = write_batch_2c_fixture(tmp_path, BATCH_2C_PATHS[0])
    content = mutate(fixture)
    path.write_text(content, encoding="utf-8")

    profile = batch_2c_profile(classify(path, tmp_path), content, tmp_path)

    assert rule in profile["missing"]
    assert main(["--root", str(tmp_path), "--profile", "batch-2c", "--fail-on-missing"]) == 1
    assert rule in capsys.readouterr().out


def test_batch_2c_topic_terms_ignore_fences_and_substrings(tmp_path: Path) -> None:
    path, fixture = write_batch_2c_fixture(tmp_path, BATCH_2C_PATHS[1])
    fenced_only = re.sub(r"\bhead\b", "header", fixture, flags=re.I)
    fenced_only += "\n```text\nhead\n```\n"
    path.write_text(fenced_only, encoding="utf-8")

    profile = batch_2c_profile(classify(path, tmp_path), path.read_text(encoding="utf-8"), tmp_path)

    assert profile["missing"] == ["topic_requirements"]
    assert has_bounded_term("HTTP header fields", "head") is False
    assert has_bounded_term("a head span", "head") is True


def test_bounded_terms_treat_underscores_as_word_characters() -> None:
    assert has_bounded_term("head_sampling", "head") is False
    assert has_bounded_term("parent_child", "parent") is False
    assert has_bounded_term("2f+1 replicas", "2f+1") is True
    assert has_bounded_term("parent/child spans", "parent/child") is True


def test_async_trace_single_message_uses_remote_parent_and_detaches_only_intentionally() -> None:
    root = Path(__file__).resolve().parents[1]
    content = (root / "docs/02-databases/22-distributed-tracing.md").read_text(encoding="utf-8")
    prose, fences, _ = parse_markdown(content)
    diagram = next(
        block for info, block in fences
        if info.split() and info.split()[0] == "mermaid" and "sequenceDiagram" in block
    )

    assert "one message; traceparent + message_id" in diagram
    assert "consumer span; parent = remote producer" in diagram
    assert "intentional detachment: new root + span links (replay/fan-in/batch)" in diagram
    assert "For one message, the consumer extracts the producer's `traceparent`" in prose
    assert re.search(
        r"Do not add a span\s+link or new root to this ordinary single-message path\.",
        prose,
    )
    assert "the worker owns a local processing parent and links to the producer" not in prose


def test_batch_2c_metadata_in_fences_is_not_metadata(tmp_path: Path) -> None:
    path, fixture = write_batch_2c_fixture(tmp_path, BATCH_2C_PATHS[0])
    visible_metadata = re.sub(r"^\*\*(?:Level|Status|Audience|Prerequisites|Sequence|Terra gate):.*$", "", fixture, flags=re.M)
    visible_metadata += """
```text
**Level:** L5
**Status:** draft
**Audience:** Engineers
**Prerequisites:** replication
**Sequence:** Batch 2C, 1/3
**Terra gate:** open
```
"""
    path.write_text(visible_metadata, encoding="utf-8")

    profile = batch_2c_profile(classify(path, tmp_path), path.read_text(encoding="utf-8"), tmp_path)

    assert profile["missing"] == ["metadata"]


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


def test_adjacent_unexplained_mermaid_blocks_are_not_explanations() -> None:
    content = """```mermaid
flowchart LR
  A --> B
```
```mermaid
flowchart LR
  B --> C
```
```mermaid
flowchart LR
  C --> D
```
"""

    assert explained_mermaid_count(content) == 0


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
