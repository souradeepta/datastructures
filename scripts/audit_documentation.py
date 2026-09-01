#!/usr/bin/env python3
"""Audit structure and educational signals in active Markdown documentation.

The scanner is intentionally dependency-free. It reports inventory metadata and
six useful signals without treating text hidden inside fenced code as prose.
The optional Batch-1, Batch-2A, and Batch-2B profiles enforce named guide
contracts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
Q_RE = re.compile(r"^\s*(?:Q(?:uestion)?\s*\d*\s*[:.)]|\d+[.)]\s+Q\b)", re.I)
EXERCISE_START_RE = re.compile(
    r"^\s{0,3}(?:#{1,6}\s*)?(?:Exercise\s+\d+\b|\d+[.)]\s+\S)", re.I
)
QA_START_RE = re.compile(
    r"^\s{0,3}(?:#{1,6}\s*)?Q(?:uestion)?\s*\d+\b", re.I
)
GUIDANCE_RE = re.compile(r"\b(?:solution|expected\s+approach|solution\s+outline|approach)\b", re.I)
ANSWER_RE = re.compile(r"\banswer\b", re.I)
FOLLOW_UP_RE = re.compile(r"\bfollow[- ]?up\b", re.I)

SIGNALS = (
    "what_why",
    "tradeoff_table",
    "mermaid",
    "code_example_fence",
    "qa",
    "short_file",
)
ENFORCED_SIGNALS = ("what_why", "tradeoff_table", "mermaid", "qa")
SHORT_FILE_LINES = 120
BATCH_1_PATHS = (
    "docs/02-databases/01-sql-advanced.md",
    "docs/02-databases/02-nosql-advanced.md",
    "docs/02-databases/03-graph-databases.md",
    "docs/02-databases/08-vector-databases.md",
    "docs/02-databases/12-distributed-transactions.md",
    "docs/02-databases/15-database-replication.md",
    "docs/02-databases/18-indexing-deep-dive.md",
    "docs/02-databases/20-change-data-capture.md",
)
BATCH_1_LINE_FLOOR = 350
BATCH_2A_PATHS = (
    "docs/02-databases/17-query-planning.md",
    "docs/02-databases/25-connection-pooling.md",
    "docs/02-databases/24-database-monitoring.md",
    "docs/02-databases/16-backup-recovery.md",
    "docs/02-databases/21-eventual-consistency.md",
    "docs/02-databases/19-sharding-advanced.md",
    "docs/02-databases/26-migration-strategies.md",
    "docs/02-databases/28-database-security.md",
)
BATCH_2A_RULES = {
    BATCH_2A_PATHS[0]: {"minimum": 400, "maximum": 550, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[1]: {"minimum": 300, "maximum": 425, "exercises": 3, "qa_min": 6, "qa_max": 8, "tables": 1},
    BATCH_2A_PATHS[2]: {"minimum": 400, "maximum": 550, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[3]: {"minimum": 400, "maximum": 550, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[4]: {"minimum": 400, "maximum": 550, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[5]: {"minimum": 450, "maximum": 600, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[6]: {"minimum": 450, "maximum": 600, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
    BATCH_2A_PATHS[7]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2},
}

BATCH_2B_PATHS = (
    "docs/02-databases/04-columnar-databases.md",
    "docs/02-databases/10-warehousing-lakehouses.md",
    "docs/02-databases/05-timeseries-databases.md",
    "docs/02-databases/29-time-series-optimization.md",
    "docs/02-databases/06-search-engines.md",
    "docs/02-databases/07-caching-stores.md",
    "docs/02-databases/11-message-queues-streams.md",
    "docs/02-databases/27-multi-tenancy.md",
)
BATCH_2B_RULES = {
    BATCH_2B_PATHS[0]: {"minimum": 450, "maximum": 600, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 1},
    BATCH_2B_PATHS[1]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 2},
    BATCH_2B_PATHS[2]: {"minimum": 450, "maximum": 600, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 3},
    BATCH_2B_PATHS[3]: {"minimum": 400, "maximum": 525, "exercises": 3, "qa_min": 6, "qa_max": 8, "tables": 1, "sequence": 4},
    BATCH_2B_PATHS[4]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 5},
    BATCH_2B_PATHS[5]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 6},
    BATCH_2B_PATHS[6]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 7},
    BATCH_2B_PATHS[7]: {"minimum": 500, "maximum": 650, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2, "sequence": 8},
}


def is_active(path: Path, root: Path) -> bool:
    """Return whether *path* is part of the repeatable active inventory."""
    relative = path.relative_to(root)
    if relative.suffix.lower() != ".md":
        return False
    if not relative.parts or relative.parts[0] not in {"docs", "learning-paths"}:
        return False
    excluded = {"_archive", "00-resources", "superpowers"}
    return not any(part in excluded for part in relative.parts)


def section_for(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    if relative.parts[0] == "learning-paths":
        return "learning-paths"
    if len(relative.parts) > 1:
        return relative.parts[1]
    return "docs"


def learning_category(path: Path, root: Path) -> str | None:
    relative = path.relative_to(root)
    if relative.parts[0] != "learning-paths":
        return None
    return relative.parts[1] if len(relative.parts) > 1 else "root"


def parse_markdown(content: str) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Return prose, fenced blocks, and headings.

    Fences are parsed line-by-line so a code example containing the words
    "What" or "Q1" does not create a prose signal. A fence is closed only by
    the same marker family (backticks or tildes).
    """
    prose: list[str] = []
    fences: list[tuple[str, str]] = []
    headings: list[str] = []
    active_marker: str | None = None
    info = ""
    block: list[str] = []
    for line in content.splitlines():
        match = FENCE_RE.match(line)
        if active_marker is None and match:
            active_marker = match.group(1)[0]
            info = match.group(2).strip().lower()
            block = []
            continue
        if active_marker is not None:
            if match and match.group(1)[0] == active_marker:
                fences.append((info, "\n".join(block)))
                active_marker = None
                info = ""
                block = []
            else:
                block.append(line)
            continue
        prose.append(line)
        heading = HEADING_RE.match(line)
        if heading:
            headings.append(heading.group(1).lower())
    if active_marker is not None:
        fences.append((info, "\n".join(block)))
    return "\n".join(prose), fences, headings


def has_tradeoff_table(prose_lines: list[str]) -> bool:
    for index, line in enumerate(prose_lines[:-1]):
        if "|" not in line or not TABLE_SEPARATOR_RE.match(prose_lines[index + 1]):
            continue
        header = line.lower()
        window = " ".join(prose_lines[max(0, index - 4):index + 2]).lower()
        if any(word in window for word in ("trade-off", "tradeoff", "advantage", "limitation", "pros", "cons")):
            return True
        if any(word in header for word in ("latency", "consistency", "complexity", "cost", "limitation", "advantage")):
            return True
    return False


def count_markdown_tables(prose_lines: list[str]) -> int:
    """Count visible Markdown table headers using their separator rows."""
    return sum(
        1
        for index, line in enumerate(prose_lines[:-1])
        if "|" in line and TABLE_SEPARATOR_RE.match(prose_lines[index + 1])
    )


def classify(path: Path, root: Path) -> dict[str, object]:
    content = path.read_text(encoding="utf-8")
    prose, fences, headings = parse_markdown(content)
    prose_lines = prose.splitlines()
    headings_text = " ".join(headings)
    visible = prose.lower()
    what = bool(re.search(r"\bwhat (?:it is|is it|are|this)\b|\bdefinition\b", visible) or re.search(r"\bwhat\b", headings_text))
    why = bool(re.search(r"\bwhy (?:it exists|it matters|this matters|use)\b|\bwhy\b", visible) or re.search(r"\bwhy\b", headings_text))
    qa = bool(re.search(r"\binterview\s+(?:q&a|questions)|\bquestions and answers\b", headings_text))
    qa = qa or sum(bool(Q_RE.match(line)) for line in prose_lines) >= 2
    mermaid = any(
        info.split() and info.split()[0] == "mermaid" for info, _ in fences
    )
    code = any(
        info.split() and info.split()[0] not in {"mermaid", ""}
        for info, _ in fences
    )
    if not code:
        code = any("```" in line or "~~~" in line for line in content.splitlines()) and not mermaid
    result = {
        "path": str(path.relative_to(root)),
        "section": section_for(path, root),
        "learning_path_category": learning_category(path, root),
        "navigation_or_index": path.name.lower() in {"readme.md", "index.md", "content_status.md"},
        "line_count": len(content.splitlines()),
        "signals": {
            "what_why": what and why,
            "tradeoff_table": has_tradeoff_table(prose_lines),
            "mermaid": mermaid,
            "code_example_fence": code,
            "qa": qa,
            "short_file": len(content.splitlines()) < SHORT_FILE_LINES,
        },
    }
    result["short_file_status"] = "short" if result["signals"]["short_file"] else "substantive"
    # short_file is a status diagnostic, not a quality failure. A code/example
    # fence is useful evidence but is intentionally not mandatory: prose-only
    # guides can still satisfy the educational contract.
    result["missing_signals"] = [
        name for name in ENFORCED_SIGNALS if not result["signals"][name]
    ]
    return result


def section_lines(content: str, title: str) -> list[str]:
    """Return visible lines in the first Markdown section named *title*."""
    prose, _, _ = parse_markdown(content)
    lines = prose.splitlines()
    wanted = title.lower()
    start = None
    section_level = 0
    for index, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading and heading.group(1).lower() == wanted:
            start = index
            section_level = len(line) - len(line.lstrip("#"))
            break
    if start is None:
        return []
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if (heading := HEADING_RE.match(lines[index]))
            and len(lines[index]) - len(lines[index].lstrip("#")) <= section_level
        ),
        len(lines),
    )
    return lines[start + 1:end]


def nearby_mermaid_explanation(content: str) -> bool:
    """Require a Mermaid block and prose immediately after its closing fence."""
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^\s*```\s*mermaid\b", line, re.I):
            continue
        close = next(
            (position for position in range(index + 1, len(lines)) if re.match(r"^\s*```\s*$", lines[position])),
            None,
        )
        if close is None:
            continue
        for following in lines[close + 1:]:
            if re.match(r"^\s*#{1,6}\s+", following):
                break
            if following.strip() and not following.strip().startswith("<!--"):
                return True
    return False


def markdown_blocks(lines: list[str], start_pattern: re.Pattern[str]) -> list[str]:
    """Split a visible section into blocks beginning at matching headings/items."""
    starts = [index for index, line in enumerate(lines) if start_pattern.match(line)]
    return [
        "\n".join(lines[start:end]).strip()
        for start, end in zip(starts, starts[1:] + [len(lines)])
    ]


def block_label(block: str, fallback: str, index: int) -> str:
    """Return a stable human-readable label for a parsed block."""
    match = re.search(r"\b(?:Exercise|Q(?:uestion)?)\s*(\d+)\b", block, re.I)
    return f"{fallback} {match.group(1) if match else index + 1}"


def batch_1_profile(item: dict[str, object], content: str) -> dict[str, object]:
    """Evaluate the declared foundational-guide contract for one guide."""
    path = str(item["path"])
    applicable = path in BATCH_1_PATHS
    if not applicable:
        return {"applicable": False, "checks": {}, "missing": []}
    objectives = section_lines(content, "Learning objectives")
    exercises = section_lines(content, "Practical exercises")
    interview = section_lines(content, "Interview Q&A")
    exercise_blocks = markdown_blocks(exercises, EXERCISE_START_RE)
    qa_blocks = markdown_blocks(interview, QA_START_RE)
    headings_text = "\n".join(parse_markdown(content)[2])
    checks = {
        "metadata": all(
            re.search(pattern, content, re.I | re.M)
            for pattern in (
                r"^\*\*Level:\*\*\s*.+$",
                r"^\*\*Status:\*\*\s*(?:draft|reviewed|tested)\b.*$",
                r"^\*\*Audience:\*\*\s*.+$",
                r"^\*\*Prerequisites:\*\*\s*.+$",
            )
        ),
        "objectives_count": 3 <= sum(bool(re.match(r"^\s*[-*]\s+", line)) for line in objectives) <= 6,
        "foundational_line_floor": int(item["line_count"]) >= BATCH_1_LINE_FLOOR,
        "topic_specific_visual": "topic-specific visual" in headings_text and nearby_mermaid_explanation(content),
        "tradeoff_table": bool(item["signals"]["tradeoff_table"]),
        "worked_example": bool(re.search(r"^\s*worked example\b", headings_text, re.I | re.M)),
        "exercise_count": len(exercise_blocks) >= 4,
        "exercise_guidance": bool(exercise_blocks) and all(GUIDANCE_RE.search(block) for block in exercise_blocks),
        "qa_count": len(qa_blocks) >= 8,
        "qa_answers": bool(qa_blocks) and all(ANSWER_RE.search(block) for block in qa_blocks),
        "qa_followups": bool(qa_blocks) and all(FOLLOW_UP_RE.search(block) for block in qa_blocks),
        "sequence": bool(re.search(r"^\*\*Sequence:\*\*\s*Batch 1,\s*\d+/8\s*$", content, re.M)),
        "terra_gate": bool(re.search(r"^\*\*Terra gate:\*\*\s*approved\s*$", content, re.M | re.I)),
        "cross_links": bool(
            re.search(r"^\s*##\s+Related and next reading\s*$", content, re.M | re.I)
            and len(re.findall(r"(?<!!\])\([^)]*\.md(?:#[^)]*)?\)", "\n".join(section_lines(content, "Related and next reading")))) >= 2
        ),
    }
    missing = [name for name, passed in checks.items() if not passed]
    failures: list[str] = []
    if not exercise_blocks:
        failures.append(f"{path}: Practical exercises has no parseable exercise blocks; add at least four numbered Exercise items.")
    else:
        for index, block in enumerate(exercise_blocks):
            if not GUIDANCE_RE.search(block):
                label = block_label(block, "Exercise", index)
                failures.append(
                    f"{path}: {label} is missing solution or expected-approach guidance; add a checkable Solution or Expected approach paragraph."
                )
    if not qa_blocks:
        failures.append(f"{path}: Interview Q&A has no parseable Q&A blocks; add at least eight Q1/Q2-style entries.")
    else:
        for index, block in enumerate(qa_blocks):
            label = block_label(block, "Q", index)
            if not ANSWER_RE.search(block):
                failures.append(f"{path}: {label} is missing an Answer; add an explicit Answer section or label.")
            if not FOLLOW_UP_RE.search(block):
                failures.append(f"{path}: {label} is missing a Follow-up; add a probing follow-up question.")
    generic_failure_messages = {
        "metadata": "add non-empty Level, Status, Audience, and Prerequisites metadata fields",
        "objectives_count": "add 3–6 bullet learning objectives",
        "foundational_line_floor": f"expand the guide to at least {BATCH_1_LINE_FLOOR} lines",
        "topic_specific_visual": "add a topic-specific Mermaid visual followed by explanatory prose",
        "tradeoff_table": "add a comparison/trade-off table with real alternatives",
        "worked_example": "add a Worked example section",
        "exercise_count": "add at least four parseable exercise blocks",
        "qa_count": "add at least eight parseable Q&A blocks",
        "sequence": "add a Sequence field in the form Batch 1, n/8",
        "terra_gate": "set the Terra gate field explicitly to approved",
        "cross_links": "add at least two Markdown links under Related and next reading",
    }
    for check in missing:
        if check in {"exercise_guidance", "qa_answers", "qa_followups"}:
            continue
        failures.append(f"{path}: {generic_failure_messages[check]}.")
    return {
        "applicable": True,
        "checks": checks,
        "missing": missing,
        "failure_messages": failures,
    }


BATCH_2A_TOPIC_REQUIREMENTS = {
    BATCH_2A_PATHS[0]: (
        "optimizer path|join decision and spill|actual rows|buffers|visibility|parameter sensitivity|stale statistics|lock waits|index concurrently",
    ),
    BATCH_2A_PATHS[1]: (
        "client-to-server|queue|checkout timeout|leak|reset|failover|arrival rate|service time|reserved|per-instance|session pooling|transaction pooling|statement pooling|PgBouncer",
    ),
    BATCH_2A_PATHS[2]: (
        "SLO|burn rate|telemetry pipeline|failure-correlation|pg_stat_database|blks_hit|blks_read|baseline|runbook",
    ),
    BATCH_2A_PATHS[3]: (
        "RPO|RTO|2 TB|5-minute|4-hour|PITR|snapshot|logical|physical|immutable|KMS|ransomware|corruption",
    ),
    BATCH_2A_PATHS[4]: (
        "multi-region|profile|version|session token|stale-read|repair|CAP|sticky|conflict|clock skew|idempotency|reconciliation|irreversible",
    ),
    BATCH_2A_PATHS[5]: (
        "tenant|order|skew|headroom|cross-shard|replica|migration bandwidth|routing and rebalance|consistent hashing|metadata|fencing|idempotent|global index|cross-shard transaction",
    ),
    BATCH_2A_PATHS[6]: (
        "expand-contract|high-write|compatibility matrix|resumable|backfill|validation|rollback boundary|deletion hold|state-machine|dual-write|outbox|CDC|DDL locking|zero downtime|full rollback",
    ),
    BATCH_2A_PATHS[7]: (
        "tenant PII|defense in depth|envelope encryption|KMS|rotation|RLS|BYPASSRLS|threat model|audit|TLS|provider",
    ),
}


def batch_2a_profile(item: dict[str, object], content: str) -> dict[str, object]:
    """Evaluate the ordered, guide-specific Batch-2A reviewed contract."""
    path = str(item["path"])
    if path not in BATCH_2A_RULES:
        return {"applicable": False, "checks": {}, "missing": []}
    rules = BATCH_2A_RULES[path]
    prose, _, headings = parse_markdown(content)
    objectives = section_lines(content, "Learning objectives")
    exercises = section_lines(content, "Practical exercises")
    interview = section_lines(content, "Interview Q&A")
    exercise_blocks = markdown_blocks(exercises, EXERCISE_START_RE)
    qa_blocks = markdown_blocks(interview, QA_START_RE)
    headings_text = "\n".join(headings)
    required_headings = (
        "what it is", "why it matters", "mental model", "worked example",
        "advantages and limitations", "topic-specific visual",
        "failure modes and operations", "practical exercises", "interview q&a",
        "related and next reading",
    )
    topic_pattern = BATCH_2A_TOPIC_REQUIREMENTS[path][0]
    checks = {
        "metadata": all(
            re.search(pattern, content, re.I | re.M)
            for pattern in (
                r"^\*\*Level:\*\*\s*.+$",
                r"^\*\*Status:\*\*\s*reviewed\s*\(\s*terra\s+pass\s*\)\s*$",
                r"^\*\*Audience:\*\*\s*.+$",
                r"^\*\*Prerequisites:\*\*\s*.+$",
                r"^\*\*Sequence:\*\*\s*Batch 2A,\s*\d+/8\s*$",
                r"^\*\*Terra gate:\*\*\s*approved\s*$",
            )
        ),
        "objectives_count": 3 <= sum(bool(re.match(r"^\s*[-*]\s+", line)) for line in objectives) <= 6,
        "line_range": rules["minimum"] <= int(item["line_count"]) <= rules["maximum"],
        "required_sections": all(title in headings_text for title in required_headings),
        "topic_requirements": all(re.search(pattern, content, re.I) for pattern in topic_pattern.split("|")),
        "topic_specific_visual": "topic-specific visual" in headings_text and nearby_mermaid_explanation(content),
        "table_count": count_markdown_tables(prose.splitlines()) >= int(rules["tables"]),
        "exercise_count": len(exercise_blocks) >= int(rules["exercises"]),
        "exercise_guidance": bool(exercise_blocks) and all(GUIDANCE_RE.search(block) for block in exercise_blocks),
        "qa_count": int(rules["qa_min"]) <= len(qa_blocks) <= int(rules["qa_max"]),
        "qa_answers": bool(qa_blocks) and all(ANSWER_RE.search(block) for block in qa_blocks),
        "qa_followups": bool(qa_blocks) and all(FOLLOW_UP_RE.search(block) for block in qa_blocks),
        "cross_links": len(re.findall(r"(?<!!\])\([^)]*\.md(?:#[^)]*)?\)", "\n".join(section_lines(content, "Related and next reading")))) >= 2,
    }
    missing = [name for name, passed in checks.items() if not passed]
    failures: list[str] = []
    if not checks["exercise_guidance"]:
        if not exercise_blocks:
            failures.append(
                f"{path}: Practical exercises has no parseable exercise blocks; add at least {rules['exercises']} numbered Exercise items with Solution or Expected approach guidance."
            )
        else:
            for index, block in enumerate(exercise_blocks):
                if not GUIDANCE_RE.search(block):
                    label = block_label(block, "Exercise", index)
                    failures.append(
                        f"{path}: {label} is missing solution or expected-approach guidance; add a checkable Solution or Expected approach paragraph."
                    )
    if not checks["qa_answers"] or not checks["qa_followups"]:
        if not qa_blocks:
            failures.append(
                f"{path}: Interview Q&A has no parseable Q&A blocks; add {rules['qa_min']}–{rules['qa_max']} Q1/Q2-style entries with explicit Answer and Follow-up labels."
            )
        else:
            for index, block in enumerate(qa_blocks):
                label = block_label(block, "Q", index)
                if not ANSWER_RE.search(block):
                    failures.append(f"{path}: {label} is missing an Answer; add an explicit Answer section or label.")
                if not FOLLOW_UP_RE.search(block):
                    failures.append(f"{path}: {label} is missing a Follow-up; add a probing follow-up question.")
    generic_failure_messages = {
        "metadata": "add non-empty Level, Status: Reviewed (Terra PASS), Audience, Prerequisites, Sequence (Batch 2A, n/8), and Terra gate (approved) metadata fields",
        "objectives_count": "add 3–6 bullet learning objectives",
        "line_range": f"keep the guide between {rules['minimum']} and {rules['maximum']} lines",
        "required_sections": "restore all required sections: What it is, Why it matters, Mental model, Worked example, Advantages and limitations, Topic-specific visual, Failure modes and operations, Practical exercises, Interview Q&A, and Related and next reading",
        "topic_requirements": "add the guide-specific topic terms and evidence required by the Batch-2A contract",
        "topic_specific_visual": "add a topic-specific Mermaid visual followed immediately by explanatory prose",
        "table_count": f"add at least {rules['tables']} Markdown comparison/trade-off table(s)",
        "exercise_count": f"add at least {rules['exercises']} parseable exercise blocks",
        "qa_count": f"add between {rules['qa_min']} and {rules['qa_max']} parseable Q&A blocks",
        "cross_links": "add at least two Markdown links under Related and next reading",
    }
    for check in missing:
        if check in {"exercise_guidance", "qa_answers", "qa_followups"}:
            continue
        failures.append(f"{path}: {generic_failure_messages[check]}.")
    return {
        "applicable": True,
        "checks": checks,
        "missing": missing,
        "failure_messages": failures,
    }


BATCH_2B_TOPIC_REQUIREMENTS = {
    BATCH_2B_PATHS[0]: (
        "row|column|segment metadata|encoding|vectorized|pruning|write cost|scan bytes|small-file|skew|mutation|version|provider",
    ),
    BATCH_2B_PATHS[1]: (
        "warehouse|data lake|lakehouse|storage|table format|CDC|backfill|Bronze|Silver|Gold|replay|late order|schema change|duplicate|partial|governance|scan|version|provider",
    ),
    BATCH_2B_PATHS[2]: (
        "sample|label|series cardinality|ingest|retention|query|alert|WAL|head|block|compaction|out-of-order|backpressure|binary|decimal|version|provider",
    ),
    BATCH_2B_PATHS[3]: (
        "chunk|compression|rollup|tier|late data|raw|fidelity|hot|warm|cold|SLO|downsampling|compaction|DST|version|provider",
    ),
    BATCH_2B_PATHS[4]: (
        "analyzer|inverted|segment|ranking|filtering|facet|refresh|shard|replica|CDC|index|rerank|product search|mapping|reindex|stale|synonym|relevance|source freshness|index visibility|ranking quality|version|provider",
    ),
    BATCH_2B_PATHS[5]: (
        "source of truth|cache-aside|write-through|write-behind|negative|TTL jitter|eviction|persistence|failover|cache miss|concurrent fill|invalidation|degraded fallback|TTL|DB protection|stampede|hot key|stale|lost write|split brain|poison|tenant leakage|version|provider",
    ),
    BATCH_2B_PATHS[6]: (
        "queue|pub/sub|durable log|event sourcing|stream processing|outbox|broker|partition|consumer group|idempotent|sink|DLQ|duplicate|retry|replay|reconciliation|ordering|at-least-once|exactly-once|side-effect|retention|schema|rebalance|offset|version|provider",
    ),
    BATCH_2B_PATHS[7]: (
        "end-to-end isolation|shared schema|RLS|schema-per-tenant|database per tenant|placement|quota|routing|onboarding|offboarding|migration|authenticated request|tenant context|pool reset|router|audit|tenant class|BYPASSRLS|owner|identifier injection|noisy neighbor|backup|deletion|drift|version|provider",
    ),
}


def explained_mermaid_count(content: str) -> int:
    """Count Mermaid blocks followed by actual prose before a new block/heading."""
    lines = content.splitlines()
    count = 0
    for index, line in enumerate(lines):
        if not re.match(r"^\s*```\s*mermaid\b", line, re.I):
            continue
        close = next(
            (position for position in range(index + 1, len(lines)) if re.match(r"^\s*```\s*$", lines[position])),
            None,
        )
        if close is None:
            continue
        for following in lines[close + 1:]:
            if re.match(r"^\s*#{1,6}\s+", following) or FENCE_RE.match(following):
                break
            if following.strip() and not following.strip().startswith("<!--"):
                count += 1
                break
    return count


def valid_related_links(path: Path, root: Path, content: str) -> int:
    """Count existing local Markdown targets in the related-reading section."""
    section = "\n".join(section_lines(content, "Related and next reading"))
    count = 0
    for target in re.findall(r"(?<!!\])\(([^)#]+(?:#[^)]*)?)\)", section):
        target_path = target.split("#", 1)[0].strip()
        if target_path and (path.parent / target_path).resolve().is_file():
            count += 1
    return count


def batch_2b_profile(item: dict[str, object], content: str, root: Path) -> dict[str, object]:
    """Evaluate the ordered Batch-2B guide contract."""
    path = str(item["path"])
    if path not in BATCH_2B_RULES:
        return {"applicable": False, "checks": {}, "missing": []}
    rules = BATCH_2B_RULES[path]
    prose, _, headings = parse_markdown(content)
    objectives = section_lines(content, "Learning objectives")
    exercises = section_lines(content, "Practical exercises")
    interview = section_lines(content, "Interview Q&A")
    exercise_blocks = markdown_blocks(exercises, EXERCISE_START_RE)
    qa_blocks = markdown_blocks(interview, QA_START_RE)
    headings_text = "\n".join(headings)
    required_headings = (
        "what it is", "why it matters", "mental model", "worked example",
        "advantages and limitations", "topic-specific visual",
        "failure modes and operations", "practical exercises", "interview q&a",
        "related and next reading",
    )
    topic_terms = BATCH_2B_TOPIC_REQUIREMENTS[path][0].split("|")
    metadata_fields = all(
        re.search(pattern, content, re.I | re.M)
        for pattern in (
            r"^\*\*Level:\*\*\s*.+$",
            r"^\*\*Audience:\*\*\s*.+$",
            r"^\*\*Prerequisites:\*\*\s*.+$",
            rf"^\*\*Sequence:\*\*\s*Batch 2B,\s*{rules['sequence']}/8\s*$",
        )
    )
    status_values = [
        value.strip().lower()
        for value in re.findall(r"^\*\*Status:\*\*\s*(.*?)\s*$", content, re.I | re.M)
    ]
    terra_gate_values = [
        value.strip().lower()
        for value in re.findall(r"^\*\*Terra gate:\*\*\s*(.*?)\s*$", content, re.I | re.M)
    ]
    metadata_state = len(status_values) == 1 and len(terra_gate_values) == 1 and (
        (status_values[0], terra_gate_values[0])
        in {("draft", "open"), ("reviewed", "approved")}
    )
    checks = {
        "metadata": metadata_fields and metadata_state,
        "objectives_count": 3 <= sum(bool(re.match(r"^\s*[-*]\s+", line)) for line in objectives) <= 6,
        "line_range": rules["minimum"] <= int(item["line_count"]) <= rules["maximum"],
        "required_sections": all(title in headings_text for title in required_headings),
        "topic_requirements": all(re.search(re.escape(term), content, re.I) for term in topic_terms),
        "mermaid_count": explained_mermaid_count(content) >= 2,
        "table_count": count_markdown_tables(prose.splitlines()) >= int(rules["tables"]),
        "exercise_count": len(exercise_blocks) >= int(rules["exercises"]),
        "exercise_guidance": len(exercise_blocks) >= int(rules["exercises"]) and all(GUIDANCE_RE.search(block) for block in exercise_blocks),
        "qa_count": int(rules["qa_min"]) <= len(qa_blocks) <= int(rules["qa_max"]),
        "qa_answers": bool(qa_blocks) and all(ANSWER_RE.search(block) for block in qa_blocks),
        "qa_followups": bool(qa_blocks) and all(FOLLOW_UP_RE.search(block) for block in qa_blocks),
        "related_links": valid_related_links(Path(path), root, content) >= 2,
    }
    missing = [name for name, passed in checks.items() if not passed]
    failures: list[str] = []
    if not checks["exercise_guidance"]:
        if not exercise_blocks:
            failures.append(f"{path}: Practical exercises has no parseable exercise blocks; add {rules['exercises']} numbered exercises with Solution or Expected approach guidance.")
        else:
            for index, block in enumerate(exercise_blocks):
                if not GUIDANCE_RE.search(block):
                    failures.append(f"{path}: {block_label(block, 'Exercise', index)} is missing solution or expected-approach guidance.")
    if not checks["qa_answers"] or not checks["qa_followups"]:
        for index, block in enumerate(qa_blocks):
            label = block_label(block, "Q", index)
            if not ANSWER_RE.search(block):
                failures.append(f"{path}: {label} is missing an Answer.")
            if not FOLLOW_UP_RE.search(block):
                failures.append(f"{path}: {label} is missing a Follow-up.")
    generic_failure_messages = {
        "metadata": "add exact draft/open or reviewed/approved metadata: Level, Status, Audience, Prerequisites, Sequence (Batch 2B n/8), and Terra gate",
        "objectives_count": "add 3–6 measurable learning-objective bullets",
        "line_range": f"keep the guide between {rules['minimum']} and {rules['maximum']} lines",
        "required_sections": "restore the ten exact Batch 2B section headings",
        "topic_requirements": "add all guide-specific technical terms required by the Batch 2B contract",
        "mermaid_count": "add at least two topic-specific Mermaid diagrams, each followed by explanatory prose",
        "table_count": f"add at least {rules['tables']} meaningful Markdown comparison tables",
        "exercise_count": f"add at least {rules['exercises']} parseable exercise blocks",
        "qa_count": f"add between {rules['qa_min']} and {rules['qa_max']} parseable Q&A blocks",
        "related_links": "add at least two existing local Markdown links under Related and next reading",
    }
    for check in missing:
        if check in {"exercise_guidance", "qa_answers", "qa_followups"}:
            continue
        failures.append(f"{path}: {generic_failure_messages[check]}.")
    return {"applicable": True, "checks": checks, "missing": missing, "failure_messages": failures}


def active_files(root: Path) -> list[Path]:
    return sorted(path for base in (root / "docs", root / "learning-paths") for path in base.rglob("*.md") if is_active(path, root))


def build_report(root: Path, profile: str | None = None) -> dict[str, object]:
    files = []
    for path in active_files(root):
        item = classify(path, root)
        if profile == "batch-1" and item["path"] in BATCH_1_PATHS:
            item["batch_1"] = batch_1_profile(item, path.read_text(encoding="utf-8"))
        if profile == "batch-2a" and item["path"] in BATCH_2A_PATHS:
            item["batch_2a"] = batch_2a_profile(item, path.read_text(encoding="utf-8"))
        if profile == "batch-2b" and item["path"] in BATCH_2B_PATHS:
            item["batch_2b"] = batch_2b_profile(item, path.read_text(encoding="utf-8"), root)
        files.append(item)
    profile_paths = (
        BATCH_1_PATHS if profile == "batch-1"
        else BATCH_2A_PATHS if profile == "batch-2a"
        else BATCH_2B_PATHS if profile == "batch-2b"
        else ()
    )
    profile_missing_paths = [
        relative
        for relative in profile_paths
        if not (root / relative).is_file()
        or not (root / relative).read_text(encoding="utf-8").strip()
    ]
    section_counts = Counter(item["section"] for item in files)
    category_counts = Counter(item["learning_path_category"] for item in files if item["learning_path_category"])
    missing_counts = Counter(signal for item in files for signal in item["missing_signals"])
    profile_key = (
        "batch_1" if profile == "batch-1"
        else "batch_2a" if profile == "batch-2a"
        else "batch_2b" if profile == "batch-2b"
        else ""
    )
    profile_missing = Counter(check for item in files for check in item.get(profile_key, {}).get("missing", [])) if profile_key else Counter()
    if profile_missing_paths:
        profile_missing["required_path"] = len(profile_missing_paths)
    profile_failures = [
        message
        for item in files
        for message in item.get(profile_key, {}).get("failure_messages", [])
    ]
    profile_failures.extend(
        f"{relative}: required {profile} guide is missing or empty; restore the file before running the strict profile."
        for relative in profile_missing_paths
    )
    return {
        "root": str(root),
        "active_markdown_files": len(files),
        "short_file_threshold_lines": SHORT_FILE_LINES,
        "section_counts": dict(sorted(section_counts.items())),
        "learning_path_category_counts": dict(sorted(category_counts.items())),
        "missing_signal_counts": dict(sorted(missing_counts.items())),
        "profile": profile,
        "profile_missing_counts": dict(sorted(profile_missing.items())),
        "profile_missing_paths": profile_missing_paths,
        "profile_failure_messages": profile_failures,
        "files": files,
    }


def print_summary(report: dict[str, object]) -> None:
    print(f"Active Markdown files: {report['active_markdown_files']}")
    print("Sections:")
    for section, count in report["section_counts"].items():
        print(f"  {section}: {count}")
    print("Missing signals:")
    for signal, count in report["missing_signal_counts"].items():
        print(f"  {signal}: {count}")
    if report.get("profile"):
        print(f"Profile: {report['profile']}")
        for check, count in report["profile_missing_counts"].items():
            print(f"  {check}: {count}")
        if report["profile_failure_messages"]:
            print("Profile failures:")
            for message in report["profile_failure_messages"]:
                print(f"  - {message}")


def print_detailed(report: dict[str, object]) -> None:
    print_summary(report)
    print("\nFiles:")
    for item in report["files"]:
        marks = ", ".join(f"{name}={'yes' if value else 'no'}" for name, value in item["signals"].items())
        print(f"- {item['path']} [{item['section']}] {item['line_count']} lines; {marks}")
        for key, label in (("batch_1", "Batch-1"), ("batch_2a", "Batch-2A"), ("batch_2b", "Batch-2B")):
            if item.get(key, {}).get("missing"):
                print(f"  {label} missing: {', '.join(item[key]['missing'])}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--summary", action="store_true", help="Print a concise inventory and signal summary")
    parser.add_argument("--detailed", action="store_true", help="Print one signal record per active file")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report suitable for CI")
    parser.add_argument("--fail-on-missing", action="store_true", help="Return nonzero if any file is missing a signal")
    parser.add_argument(
        "--profile", choices=("batch-1", "batch-2a", "batch-2b"), help="Apply a named strict guide profile"
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = build_report(args.root.resolve(), args.profile)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif args.detailed:
        print_detailed(report)
    else:
        print_summary(report)
    profile_key = (
        "batch_1" if args.profile == "batch-1"
        else "batch_2a" if args.profile == "batch-2a"
        else "batch_2b" if args.profile == "batch-2b"
        else ""
    )
    profile_failed = bool(report.get("profile_missing_paths")) or any(
        item.get(profile_key, {}).get("missing") for item in report["files"]
    ) if profile_key else False
    standard_failed = any(item["missing_signals"] for item in report["files"])
    if args.fail_on_missing and (profile_failed if args.profile else standard_failed):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
