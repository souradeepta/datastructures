"""A small read/write quorum register for interview practice.

This is an in-memory model: replicas fail by being marked unavailable and a
coordinator synchronously contacts a deterministic subset of replicas.
"""

from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Hashable, Iterable


@dataclass(frozen=True)
class VersionedValue:
    """A value with a monotonically increasing per-key version."""

    version: int
    value: Any


class QuorumRegister:
    """Replicated register using configurable read and write quorums.

    A write succeeds only when at least ``write_quorum`` replicas are
    available. A read contacts ``read_quorum`` available replicas, chooses the
    newest version, and repairs stale responses in that read set. The default
    configuration requires ``R + W > N`` so a completed write and read share a
    replica; this is a safety precondition, not a proof of linearizability.
    """

    def __init__(
        self,
        replicas: Iterable[Hashable],
        read_quorum: int,
        write_quorum: int,
    ) -> None:
        self._replicas = tuple(replicas)
        if not self._replicas or len(set(self._replicas)) != len(self._replicas):
            raise ValueError("replicas must be non-empty and unique")
        n = len(self._replicas)
        if not 1 <= read_quorum <= n or not 1 <= write_quorum <= n:
            raise ValueError("quorums must be between 1 and replica count")
        if read_quorum + write_quorum <= n:
            raise ValueError("read_quorum + write_quorum must be greater than N")
        self.read_quorum = read_quorum
        self.write_quorum = write_quorum
        self._available = set(self._replicas)
        self._data: dict[Hashable, dict[Hashable, VersionedValue]] = {
            replica: {} for replica in self._replicas
        }
        self._versions: dict[Hashable, int] = {}

    @property
    def replicas(self) -> tuple[Hashable, ...]:
        return self._replicas

    @property
    def available_replicas(self) -> tuple[Hashable, ...]:
        return tuple(replica for replica in self._replicas if replica in self._available)

    def set_replica_available(self, replica: Hashable, available: bool) -> None:
        if replica not in self._data:
            raise KeyError(replica)
        if available:
            self._available.add(replica)
        else:
            self._available.discard(replica)

    def write(self, key: Hashable, value: Any) -> VersionedValue:
        available = self.available_replicas
        if len(available) < self.write_quorum:
            raise RuntimeError("write quorum is unavailable")
        version = self._versions.get(key, 0) + 1
        record = VersionedValue(version, deepcopy(value))
        self._versions[key] = version
        for replica in available[: self.write_quorum]:
            self._data[replica][key] = record
        return VersionedValue(record.version, deepcopy(record.value))

    def read(self, key: Hashable) -> VersionedValue | None:
        available = self.available_replicas
        if len(available) < self.read_quorum:
            raise RuntimeError("read quorum is unavailable")
        contacted = available[: self.read_quorum]
        records = [self._data[replica][key] for replica in contacted if key in self._data[replica]]
        if not records:
            return None
        newest = max(records, key=lambda record: record.version)
        for replica in contacted:
            current = self._data[replica].get(key)
            if current is None or current.version < newest.version:
                self._data[replica][key] = newest
        return VersionedValue(newest.version, deepcopy(newest.value))

    def replica_value(self, replica: Hashable, key: Hashable) -> VersionedValue | None:
        if replica not in self._data:
            raise KeyError(replica)
        record = self._data[replica].get(key)
        return None if record is None else VersionedValue(record.version, deepcopy(record.value))
