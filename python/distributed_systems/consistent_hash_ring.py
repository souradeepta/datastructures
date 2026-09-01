"""Deterministic consistent hashing with virtual nodes."""

from __future__ import annotations

import bisect
import hashlib
from typing import Hashable, Iterable


class ConsistentHashRing:
    """Route keys around a SHA-256 ring and expose a migration plan.

    Node names are strings because they form part of the stable hash input.
    ``migration_plan`` compares an old assignment supplied by the caller with
    the current ring, making node additions and removals measurable.
    """

    def __init__(self, nodes: Iterable[str] = (), virtual_nodes: int = 100) -> None:
        if not isinstance(virtual_nodes, int) or isinstance(virtual_nodes, bool) or virtual_nodes < 1:
            raise ValueError("virtual_nodes must be a positive integer")
        self.virtual_nodes = virtual_nodes
        self._nodes: list[str] = []
        self._ring: list[tuple[int, str]] = []
        for node in nodes:
            self.add_node(node)

    @staticmethod
    def _hash(value: str) -> int:
        return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest(), "big")

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(self._nodes)

    def _rebuild(self) -> None:
        points = []
        for node in self._nodes:
            for index in range(self.virtual_nodes):
                points.append((self._hash(f"{node}#{index}"), node))
        self._ring = sorted(points)

    def add_node(self, node: str) -> None:
        if not isinstance(node, str) or not node:
            raise ValueError("node must be a non-empty string")
        if node in self._nodes:
            raise ValueError(f"node already exists: {node}")
        self._nodes.append(node)
        self._nodes.sort()
        self._rebuild()

    def remove_node(self, node: str) -> None:
        if node not in self._nodes:
            raise KeyError(node)
        self._nodes.remove(node)
        self._rebuild()

    def _start_index(self, key: str) -> int:
        if not self._ring:
            raise RuntimeError("cannot route with an empty ring")
        point = self._hash(key)
        index = bisect.bisect_left(self._ring, (point, ""))
        return index % len(self._ring)

    def get_node(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        return self._ring[self._start_index(key)][1]

    def get_replicas(self, key: str, count: int) -> tuple[str, ...]:
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise ValueError("count must be a positive integer")
        if not self._ring:
            raise RuntimeError("cannot route with an empty ring")
        result: list[str] = []
        index = self._start_index(key)
        for offset in range(len(self._ring)):
            node = self._ring[(index + offset) % len(self._ring)][1]
            if node not in result:
                result.append(node)
            if len(result) == min(count, len(self._nodes)):
                break
        return tuple(result)

    def migration_plan(
        self, keys: Iterable[str], previous_assignments: dict[str, str]
    ) -> dict[str, tuple[str | None, str]]:
        """Return ``key -> (old_node, new_node)`` for supplied keys."""
        plan = {}
        for key in keys:
            new_node = self.get_node(key)
            plan[key] = (previous_assignments.get(key), new_node)
        return plan
