"""Central definitions for documentation review and audit profiles.

This module contains data only.  The scanner owns parsing and evaluation; this
module owns profile identity, paths, thresholds, and future-cohort planning.
Keeping those concerns separate lets callers import the established path
constants without importing the command-line scanner or changing its behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ProfileDefinition:
    """Describe a cohort without deciding whether it is ready for automation."""

    name: str
    report_key: str
    paths: tuple[str, ...]
    rules: Mapping[str, Mapping[str, int]]
    enabled: bool
    status: str
    description: str


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
BATCH_1_RULES = {path: {"minimum": BATCH_1_LINE_FLOOR} for path in BATCH_1_PATHS}

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

# These are the three remaining database guides.  They are deliberately
# registered as open planning targets; no guide content is upgraded by this
# module and no future profile is a CI gate.
BATCH_2C_PATHS = (
    "docs/02-databases/13-consensus-algorithms.md",
    "docs/02-databases/22-distributed-tracing.md",
    "docs/02-databases/30-stream-processing.md",
)
BATCH_2C_RULES = {
    path: {"sequence": index, "exercises": 4, "qa_min": 8, "qa_max": 10, "tables": 2}
    for index, path in enumerate(BATCH_2C_PATHS, 1)
}

BATCH_3A_PATHS = (
    "docs/04-ai-ml-llms/06-rag-systems.md",
    "docs/04-ai-ml-llms/08-model-serving-inference.md",
    "docs/04-ai-ml-llms/12-nlp-advanced.md",
    "docs/04-ai-ml-llms/16-cost-optimization.md",
    "docs/04-ai-ml-llms/22-model-rollouts-and-serving.md",
)
BATCH_3A_RULES = {path: {} for path in BATCH_3A_PATHS}

# Batch 4A is intentionally a small routing-surface cohort: two learning
# paths and two high-use interview frameworks.  The remaining paths/frameworks
# stay open for later selection.
BATCH_4A_PATHS = (
    "learning-paths/sequential-tracks/4-week-focused.md",
    "learning-paths/interview-playbooks/system-design-round.md",
    "docs/01-interview-frameworks/coding-interview-framework.md",
    "docs/01-interview-frameworks/system-design-interview-guide.md",
)
BATCH_4A_RULES = {path: {} for path in BATCH_4A_PATHS}

# Batch 5 is a debt-review scaffold, not a claim that the selected catalog is
# reviewed.  These representative cohorts are kept small until the human
# reviewer decides the next system-design slice.
BATCH_5_PATHS = (
    "docs/03-system-design/16-networking/17_ospf_routing.md",
    "docs/03-system-design/03-design-patterns/01_singleton.md",
    "docs/03-system-design/06-data-systems/19_database_sharding.md",
)
BATCH_5_RULES = {path: {} for path in BATCH_5_PATHS}
BATCH_5_SELECTED_COHORTS = {
    "distributed-systems": "docs/03-system-design/04-distributed-systems/",
    "data-systems": "docs/03-system-design/06-data-systems/",
    "networking-debt": "docs/03-system-design/16-networking/",
}


PROFILE_DEFINITIONS = {
    "batch-1": ProfileDefinition(
        "batch-1", "batch_1", BATCH_1_PATHS, BATCH_1_RULES, True, "established",
        "Terra-approved foundational database guides.",
    ),
    "batch-2a": ProfileDefinition(
        "batch-2a", "batch_2a", BATCH_2A_PATHS, BATCH_2A_RULES, True, "established",
        "Terra-approved database operations and scale guides.",
    ),
    "batch-2b": ProfileDefinition(
        "batch-2b", "batch_2b", BATCH_2B_PATHS, BATCH_2B_RULES, True, "established",
        "Terra-approved analytical data and tenant-boundary guides.",
    ),
    "batch-2c": ProfileDefinition(
        "batch-2c", "batch_2c", BATCH_2C_PATHS, BATCH_2C_RULES, False, "open",
        "Open three-guide database follow-on: consensus, tracing, and streaming.",
    ),
    "batch-3a": ProfileDefinition(
        "batch-3a", "batch_3a", BATCH_3A_PATHS, BATCH_3A_RULES, False, "open",
        "Open ML/AI foundations cohort; human review and lab reconciliation remain open.",
    ),
    "batch-4a": ProfileDefinition(
        "batch-4a", "batch_4a", BATCH_4A_PATHS, BATCH_4A_RULES, False, "open",
        "Open learning-path and interview-framework routing cohort.",
    ),
    "batch-5": ProfileDefinition(
        "batch-5", "batch_5", BATCH_5_PATHS, BATCH_5_RULES, False, "open",
        "Open selected system-design debt cohorts; 27/134 remains the debt baseline.",
    ),
}

ESTABLISHED_PROFILES = tuple(name for name, profile in PROFILE_DEFINITIONS.items() if profile.enabled)
FUTURE_PROFILES = tuple(name for name, profile in PROFILE_DEFINITIONS.items() if not profile.enabled)
PROFILE_NAMES = tuple(PROFILE_DEFINITIONS)


def profile_definition(name: str) -> ProfileDefinition:
    """Return a named definition or raise a useful error for callers."""
    try:
        return PROFILE_DEFINITIONS[name]
    except KeyError as exc:
        raise KeyError(f"unknown documentation profile: {name}") from exc


BATCH_2A_TOPIC_REQUIREMENTS = {
    BATCH_2A_PATHS[0]: ("optimizer path|join decision and spill|actual rows|buffers|visibility|parameter sensitivity|stale statistics|lock waits|index concurrently",),
    BATCH_2A_PATHS[1]: ("client-to-server|queue|checkout timeout|leak|reset|failover|arrival rate|service time|reserved|per-instance|session pooling|transaction pooling|statement pooling|PgBouncer",),
    BATCH_2A_PATHS[2]: ("SLO|burn rate|telemetry pipeline|failure-correlation|pg_stat_database|blks_hit|blks_read|baseline|runbook",),
    BATCH_2A_PATHS[3]: ("RPO|RTO|2 TB|5-minute|4-hour|PITR|snapshot|logical|physical|immutable|KMS|ransomware|corruption",),
    BATCH_2A_PATHS[4]: ("multi-region|profile|version|session token|stale-read|repair|CAP|sticky|conflict|clock skew|idempotency|reconciliation|irreversible",),
    BATCH_2A_PATHS[5]: ("tenant|order|skew|headroom|cross-shard|replica|migration bandwidth|routing and rebalance|consistent hashing|metadata|fencing|idempotent|global index|cross-shard transaction",),
    BATCH_2A_PATHS[6]: ("expand-contract|high-write|compatibility matrix|resumable|backfill|validation|rollback boundary|deletion hold|state-machine|dual-write|outbox|CDC|DDL locking|zero downtime|full rollback",),
    BATCH_2A_PATHS[7]: ("tenant PII|defense in depth|envelope encryption|KMS|rotation|RLS|BYPASSRLS|threat model|audit|TLS|provider",),
}

BATCH_2B_TOPIC_REQUIREMENTS = {
    BATCH_2B_PATHS[0]: ("row|column|segment metadata|encoding|vectorized|pruning|write cost|scan bytes|small-file|skew|mutation|version|provider",),
    BATCH_2B_PATHS[1]: ("warehouse|data lake|lakehouse|storage|table format|CDC|backfill|Bronze|Silver|Gold|replay|late order|schema change|duplicate|partial|governance|scan|version|provider",),
    BATCH_2B_PATHS[2]: ("sample|label|series cardinality|ingest|retention|query|alert|WAL|head|block|compaction|out-of-order|backpressure|binary|decimal|version|provider",),
    BATCH_2B_PATHS[3]: ("chunk|compression|rollup|tier|late data|raw|fidelity|hot|warm|cold|SLO|downsampling|compaction|DST|version|provider",),
    BATCH_2B_PATHS[4]: ("analyzer|inverted|segment|ranking|filtering|facet|refresh|shard|replica|CDC|index|rerank|product search|mapping|reindex|stale|synonym|relevance|source freshness|index visibility|ranking quality|version|provider",),
    BATCH_2B_PATHS[5]: ("source of truth|cache-aside|write-through|write-behind|negative|TTL jitter|eviction|persistence|failover|cache miss|concurrent fill|invalidation|degraded fallback|TTL|DB protection|stampede|hot key|stale|lost write|split brain|poison|tenant leakage|version|provider",),
    BATCH_2B_PATHS[6]: ("queue|pub/sub|durable log|event sourcing|stream processing|outbox|broker|partition|consumer group|idempotent|sink|DLQ|duplicate|retry|replay|reconciliation|ordering|at-least-once|exactly-once|side-effect|retention|schema|rebalance|offset|version|provider",),
    BATCH_2B_PATHS[7]: ("end-to-end isolation|shared schema|RLS|schema-per-tenant|database per tenant|placement|quota|routing|onboarding|offboarding|migration|authenticated request|tenant context|pool reset|router|audit|tenant class|BYPASSRLS|owner|identifier injection|noisy neighbor|backup|deletion|drift|version|provider",),
}
