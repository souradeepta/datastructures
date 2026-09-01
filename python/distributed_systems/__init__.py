"""Dependency-free distributed-systems teaching models."""

from .consistent_hash_ring import ConsistentHashRing
from .event_time_windows import Event, EventTimeWindows, WindowResult
from .quorum_register import QuorumRegister, VersionedValue

__all__ = [
    "ConsistentHashRing",
    "Event",
    "EventTimeWindows",
    "QuorumRegister",
    "VersionedValue",
    "WindowResult",
]
